from typing import List
from pydantic import BaseModel, Field


class ProductAgentOutput(BaseModel):
    summary: str = Field(description="Short meeting summary focused on product concerns.")
    action_items: List[str] = Field(description="Concrete action items from the meeting.")
    risks: List[str] = Field(description="Product or delivery risks identified in the meeting.")
    recommendations: List[str] = Field(description="Practical recommendations for next steps.")
    confidence_score: float = Field(description="A value between 0 and 1 representing confidence.")