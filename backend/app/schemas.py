from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TranscriptAnalyzeRequest(BaseModel):
    meeting_title: Optional[str] = None
    transcript: str = Field(..., min_length=20, description="Meeting transcript text")


class AnalyzeResponse(BaseModel):
    meeting_id: Optional[str] = None
    created_at: Optional[str] = None
    version: str = "1.0"

    meeting_title: Optional[str] = None
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
    consensus_factors: List[str]
    consensus_reason: str

    meeting_health_score: int
    meeting_health_label: str

    processing_time_seconds: float
    agent_timings: Dict[str, float]

    executive_summary: str
    final_decision: str
    priority_actions: List[str]
    overall_risk_level: str
    coordinator_notes: List[str]