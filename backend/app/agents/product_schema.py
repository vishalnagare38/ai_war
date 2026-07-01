from typing import List
from pydantic import BaseModel, Field


class ProductAgentOutput(BaseModel):

    summary: str = Field(
        description="Executive summary."
    )

    action_items: List[str] = Field(
        default_factory=list,
        max_length=5,
    )

    risks: List[str] = Field(
        default_factory=list,
        max_length=5,
    )

    recommendations: List[str] = Field(
        default_factory=list,
        max_length=5,
    )

    confidence_score: float = Field(
        ge=0,
        le=1,
    )