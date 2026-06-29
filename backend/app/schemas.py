from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TranscriptAnalyzeRequest(BaseModel):
    meeting_title: Optional[str] = None
    transcript: str = Field(
        ...,
        min_length=20,
        description="Meeting transcript text",
    )


class AnalyzeResponse(BaseModel):

    # ===============================
    # Metadata
    # ===============================

    meeting_id: Optional[str] = None
    created_at: Optional[str] = None
    version: str = "1.0"

    meeting_title: Optional[str] = None

    # ===============================
    # Product Agent
    # ===============================

    summary: str
    action_items: List[str]
    risks: List[str]
    recommendations: List[str]
    confidence_score: float
    agent_used: str

    # ===============================
    # Engineering Agent
    # ===============================

    engineering_insights: List[str]
    engineering_risks: List[str]
    engineering_recommendations: List[str]

    # ===============================
    # Finance Agent
    # ===============================

    finance_insights: List[str]
    finance_risks: List[str]
    finance_recommendations: List[str]

    # ===============================
    # Risk Agent
    # ===============================

    risk_insights: List[str]
    risk_level: str
    risk_recommendations: List[str]

    # ===============================
    # ML Model
    # ===============================

    ml_risk_probability: float
    ml_risk_label: str
    delay_likelihood: float

    # ===============================
    # Consensus Engine
    # ===============================

    consensus_score: float
    agent_agreement: str
    consensus_factors: List[str]
    consensus_reason: str

    # ===============================
    # Meeting Health
    # ===============================

    meeting_health_score: int
    meeting_health_label: str

    # ===============================
    # Project Intelligence
    # ===============================

    history_summary: str
    recurring_blockers: List[str]
    risk_trend: List[str]
    health_trend: List[int]
    project_momentum: str

    # ===============================
    # Performance
    # ===============================

    processing_time_seconds: float
    agent_timings: Dict[str, float]

    timeline: List[Dict] = Field(default_factory=list)

    # ===============================
    # Coordinator
    # ===============================

    executive_summary: str
    final_decision: str
    priority_actions: List[str]
    overall_risk_level: str
    coordinator_notes: List[str]


class DashboardResponse(BaseModel):

    total_meetings: int

    average_health: float

    average_risk_probability: float

    high_risk_meetings: int

    healthy_meetings: int

    history_summary: str

    recurring_blockers: List[str]

    risk_trend: List[str]

    health_trend: List[int]

    project_momentum: str