from typing import TypedDict, Optional, List, Dict, Any


class MeetingState(TypedDict, total=False):
    meeting_title: Optional[str]
    transcript: str

    # Product Agent
    summary: str
    action_items: List[str]
    risks: List[str]
    recommendations: List[str]
    confidence_score: float
    agent_used: str

    # Engineering Agent
    engineering_insights: List[str]
    engineering_risks: List[str]
    engineering_recommendations: List[str]

    # Finance Agent
    finance_insights: List[str]
    finance_risks: List[str]
    finance_recommendations: List[str]

    # Risk Agent
    risk_insights: List[str]
    risk_level: str
    risk_recommendations: List[str]

    # ML
    ml_risk_probability: float
    ml_risk_label: str
    delay_likelihood: float

    # Consensus
    consensus_score: float
    agent_agreement: str
    consensus_factors: List[str]
    consensus_reason: str

    # Meeting Health
    meeting_health_score: int
    meeting_health_label: str

    # Timing
    agent_timings: Dict[str, float]
    timeline: List[Dict[str, Any]]
    processing_time_seconds: float

    # Coordinator
    executive_summary: str
    final_decision: str
    priority_actions: List[str]
    overall_risk_level: str
    coordinator_notes: List[str]
    
    history_summary: str
    recurring_blockers: List[str]
    risk_trend: str
    health_trend: str
    project_momentum: str