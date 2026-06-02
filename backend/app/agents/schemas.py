from typing import List
from pydantic import BaseModel, Field


class EngineeringAgentOutput(BaseModel):
    engineering_insights: List[str] = Field(default_factory=list)
    engineering_risks: List[str] = Field(default_factory=list)
    engineering_recommendations: List[str] = Field(default_factory=list)


class FinanceAgentOutput(BaseModel):
    finance_insights: List[str] = Field(default_factory=list)
    finance_risks: List[str] = Field(default_factory=list)
    finance_recommendations: List[str] = Field(default_factory=list)


class RiskAgentOutput(BaseModel):
    risk_insights: List[str] = Field(default_factory=list)
    risk_level: str = Field(default="low")
    risk_recommendations: List[str] = Field(default_factory=list)


class CoordinatorAgentOutput(BaseModel):
    executive_summary: str
    final_decision: str
    priority_actions: List[str] = Field(default_factory=list)
    overall_risk_level: str = Field(default="low")
    coordinator_notes: List[str] = Field(default_factory=list)