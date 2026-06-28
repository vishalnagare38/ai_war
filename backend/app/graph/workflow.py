from concurrent.futures import ThreadPoolExecutor
import time

from langgraph.graph import END, StateGraph

from app.graph.state import MeetingState
from app.graph.consensus import consensus_node

from app.agents.product import ProductAgent
from app.agents.engineering import EngineeringAgent
from app.agents.finance import FinanceAgent
from app.agents.risk import RiskAgent
from app.agents.coordinator import CoordinatorAgent

from app.ml.risk_scorer import RiskScorer


product_agent = ProductAgent()
engineering_agent = EngineeringAgent()
finance_agent = FinanceAgent()
risk_agent = RiskAgent()
coordinator_agent = CoordinatorAgent()
risk_scorer = RiskScorer()


def product_node(state: MeetingState) -> MeetingState:
    transcript = state["transcript"]
    timings = dict(state.get("agent_timings", {}))

    start = time.perf_counter()
    result = product_agent.analyze(transcript)
    timings["Product Agent"] = round(time.perf_counter() - start, 2)

    return {
        **state,
        **result,
        "agent_timings": timings,
    }


def specialist_parallel_node(state: MeetingState) -> MeetingState:
    transcript = state["transcript"]
    timings = dict(state.get("agent_timings", {}))

    def run_engineering():
        start = time.perf_counter()

        result = engineering_agent.analyze(transcript)

        duration = max(
            round(time.perf_counter() - start, 3),
            0.01,
        )

        return result, duration


    def run_finance():
        start = time.perf_counter()

        result = finance_agent.analyze(transcript)

        duration = max(
            round(time.perf_counter() - start, 3),
            0.01,
        )

        return result, duration


    def run_ml():
        start = time.perf_counter()

        result = risk_scorer.predict(transcript)

        duration = max(
            round(time.perf_counter() - start, 3),
            0.01,
        )

        result.duration = duration

        return result, duration

    with ThreadPoolExecutor(max_workers=3) as executor:
        eng_future = executor.submit(run_engineering)
        fin_future = executor.submit(run_finance)
        ml_future = executor.submit(run_ml)

        engineering_result, eng_time = eng_future.result()
        finance_result, fin_time = fin_future.result()
        ml_prediction, ml_time = ml_future.result()

    timings["Engineering Agent"] = eng_time
    timings["Finance Agent"] = fin_time
    timings["ML Scorer"] = ml_time

    risk_start = time.perf_counter()
    risk_result = risk_agent.analyze(transcript, ml_prediction.probability)
    timings["Risk Agent"] = round(time.perf_counter() - risk_start, 2)

    return {
        **state,
        **engineering_result,
        **finance_result,
        **risk_result,
        "ml_risk_probability": ml_prediction.probability,
        "ml_risk_label": ml_prediction.label,
        "delay_likelihood": ml_prediction.delay_likelihood,
        "agent_timings": timings,
    }


def consensus_wrapper(state: MeetingState) -> MeetingState:
    timings = dict(state.get("agent_timings", {}))

    start = time.perf_counter()
    result = consensus_node(state)
    timings["Consensus Engine"] = round(time.perf_counter() - start, 2)

    return {
        **state,
        **result,
        "agent_timings": timings,
    }


def coordinator_node(state: MeetingState) -> MeetingState:
    timings = dict(state.get("agent_timings", {}))

    start = time.perf_counter()
    result = coordinator_agent.analyze(state)
    timings["Coordinator Agent"] = round(time.perf_counter() - start, 2)

    return {
        **state,
        **result,
        "agent_timings": timings,
    }


def build_workflow():
    graph = StateGraph(MeetingState)

    graph.add_node("product_agent", product_node)
    graph.add_node("specialist_parallel", specialist_parallel_node)
    graph.add_node("consensus_agent", consensus_wrapper)
    graph.add_node("coordinator_agent", coordinator_node)

    graph.set_entry_point("product_agent")
    graph.add_edge("product_agent", "specialist_parallel")
    graph.add_edge("specialist_parallel", "consensus_agent")
    graph.add_edge("consensus_agent", "coordinator_agent")
    graph.add_edge("coordinator_agent", END)

    return graph.compile()