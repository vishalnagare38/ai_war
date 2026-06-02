from pydantic import BaseModel, Field
from typing import List, Optional


class TranscriptAnalyzeRequest(BaseModel):
    meeting_title: Optional[str] = None
    transcript: str = Field(..., min_length=20, description="Meeting transcript text")


class AnalyzeResponse(BaseModel):
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

    executive_summary: str
    final_decision: str
    priority_actions: List[str]
    overall_risk_level: str
    coordinator_notes: List[str]