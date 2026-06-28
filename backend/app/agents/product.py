from typing import Dict
import time

from app.agents.product_schema import ProductAgentOutput
from app.llm.structured import call_structured_gemini


class ProductAgent:
    def analyze(self, transcript: str) -> Dict[str, object]:
        start = time.time()

        prompt = f"""
You are the Product Agent in a multi-agent meeting analysis system.

Analyze the meeting transcript and return:
- summary
- action_items
- risks
- recommendations
- confidence_score

Rules:
- Focus on product delivery and execution.
- Be concise and specific.
- Do not hallucinate.
- Return only information supported by the transcript.

Transcript:
{transcript}
""".strip()

        parsed = call_structured_gemini(prompt, ProductAgentOutput)

        return {
            "summary": parsed.summary,
            "action_items": parsed.action_items,
            "risks": parsed.risks,
            "recommendations": parsed.recommendations,
            "confidence_score": parsed.confidence_score,
            "agent_used": "ProductAgent-LLM",
            "_duration": round(time.time() - start, 2),
        }