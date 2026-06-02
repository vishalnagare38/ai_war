from langgraph.graph import StateGraph, END
from app.graph.state import MeetingState
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


def engineering_node(state: MeetingState) -> MeetingState:
    transcript = state.get("transcript", "")
    result = engineering_agent.analyze(transcript)
    return {**state, **result}


def finance_node(state: MeetingState) -> MeetingState:
    transcript = state.get("transcript", "")
    result = finance_agent.analyze(transcript)
    return {**state, **result}


def risk_node(state: MeetingState) -> MeetingState:
    transcript = state.get("transcript", "")
    result = risk_agent.analyze(transcript)
    return {**state, **result}


def ml_risk_node(state: MeetingState) -> MeetingState:
    transcript = state.get("transcript", "")
    prediction = risk_scorer.predict(transcript)

    return {
        **state,
        "ml_risk_probability": prediction.probability,
        "ml_risk_label": prediction.label,
        "delay_likelihood": prediction.delay_likelihood,
    }


def coordinator_node(state: MeetingState) -> MeetingState:
    result = coordinator_agent.analyze(state)
    return {**state, **result}


def build_workflow():
    graph = StateGraph(MeetingState)

    graph.add_node("product_agent", product_node)
    graph.add_node("engineering_agent", engineering_node)
    graph.add_node("finance_agent", finance_node)
    graph.add_node("risk_agent", risk_node)
    graph.add_node("ml_risk_scorer", ml_risk_node)
    graph.add_node("coordinator_agent", coordinator_node)

    graph.set_entry_point("product_agent")
    graph.add_edge("product_agent", "engineering_agent")
    graph.add_edge("engineering_agent", "finance_agent")
    graph.add_edge("finance_agent", "risk_agent")
    graph.add_edge("risk_agent", "ml_risk_scorer")
    graph.add_edge("ml_risk_scorer", "coordinator_agent")
    graph.add_edge("coordinator_agent", END)

    return graph.compile()