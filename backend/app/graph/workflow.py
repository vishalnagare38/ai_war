from concurrent.futures import ThreadPoolExecutor

from langgraph.graph import StateGraph, END

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
    transcript = state.get("transcript", "")
    result = product_agent.analyze(transcript)
    return {**state, **result}


def specialist_parallel_node(state: MeetingState) -> MeetingState:
    transcript = state.get("transcript", "")

    with ThreadPoolExecutor(max_workers=4) as executor:
        eng_future = executor.submit(engineering_agent.analyze, transcript)
        fin_future = executor.submit(finance_agent.analyze, transcript)
        ml_future = executor.submit(risk_scorer.predict, transcript)

        engineering_result = eng_future.result()
        finance_result = fin_future.result()
        ml_prediction = ml_future.result()

        risk_result = risk_agent.analyze(
            transcript,
            ml_prediction.probability
        )

    return {
        **state,
        **engineering_result,
        **finance_result,
        **risk_result,
        "ml_risk_probability": ml_prediction.probability,
        "ml_risk_label": ml_prediction.label,
        "delay_likelihood": ml_prediction.delay_likelihood,
    }


def coordinator_node(state: MeetingState) -> MeetingState:
    result = coordinator_agent.analyze(state)
    return {**state, **result}


def build_workflow():
    graph = StateGraph(MeetingState)

    graph.add_node("product_agent", product_node)
    graph.add_node("specialist_parallel", specialist_parallel_node)
    graph.add_node("consensus_agent", consensus_node)
    graph.add_node("coordinator_agent", coordinator_node)

    graph.set_entry_point("product_agent")
    graph.add_edge("product_agent", "specialist_parallel")
    graph.add_edge("specialist_parallel", "consensus_agent")
    graph.add_edge("consensus_agent", "coordinator_agent")
    graph.add_edge("coordinator_agent", END)

    return graph.compile()