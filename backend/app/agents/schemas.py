from typing import List
from pydantic import BaseModel, Field


class EngineeringAgentOutput(BaseModel):

    engineering_insights: List[str] = Field(
        default_factory=list,
        max_length=5,
    )

    engineering_risks: List[str] = Field(
        default_factory=list,
        max_length=5,
    )

    engineering_recommendations: List[str] = Field(
        default_factory=list,
        max_length=5,
    )


class FinanceAgentOutput(BaseModel):

    finance_insights: List[str] = Field(
        default_factory=list,
        max_length=5,
    )

    finance_risks: List[str] = Field(
        default_factory=list,
        max_length=5,
    )

    finance_recommendations: List[str] = Field(
        default_factory=list,
        max_length=5,
    )


class RiskAgentOutput(BaseModel):

    risk_insights: List[str] = Field(
        default_factory=list,
        max_length=6,
    )

    risk_level: str = Field(
        default="low",
    )

    risk_recommendations: List[str] = Field(
        default_factory=list,
        max_length=6,
    )

class CoordinatorAgentOutput(BaseModel):

    executive_summary: str

    final_decision: str

    priority_actions: List[str] = Field(
        default_factory=list,
        max_length=6,
    )

    overall_risk_level: str = Field(
        default="low",
    )

    coordinator_notes: List[str] = Field(
        default_factory=list,
        max_length=4,
    )