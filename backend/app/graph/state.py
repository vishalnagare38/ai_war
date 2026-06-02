from typing import TypedDict, Optional, List


class MeetingState(TypedDict, total=False):
    meeting_title: Optional[str]
    transcript: str

    summary: str
    action_items: List[str]
    risks: List[str]
    recommendations: List[str]
    confidence_score: float
    agent_used: str

    engineering_insights: List[str]
    engineering_risks: List[str]
    engineering_recommendations: List[str]

    finance_insights: List[str]
    finance_risks: List[str]
    finance_recommendations: List[str]

    risk_insights: List[str]
    risk_level: str
    risk_recommendations: List[str]

    ml_risk_probability: float
    ml_risk_label: str
    delay_likelihood: float

    consensus_score: float
    agent_agreement: str

    executive_summary: str
    final_decision: str
    priority_actions: List[str]
    overall_risk_level: str
    coordinator_notes: List[str]

    processing_time_seconds: float