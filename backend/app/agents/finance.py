from typing import Dict
import time

from app.agents.schemas import FinanceAgentOutput
from app.llm.structured import call_structured_gemini


class FinanceAgent:
    def analyze(self, transcript: str) -> Dict[str, object]:
        start = time.time()

        prompt = f"""
You are the Finance Agent in a multi-agent meeting analysis system.

Analyze the transcript from a finance perspective and return:
- finance_insights
- finance_risks
- finance_recommendations

Rules:
- Be concise and specific.
- Only use information supported by the transcript.
- Return valid JSON only.

Transcript:
{transcript}
""".strip()

        parsed = call_structured_gemini(prompt, FinanceAgentOutput)

        return {
            **parsed.model_dump(),
            "agent_used": "FinanceAgent-LLM",
            "_duration": round(time.time() - start, 2),
        }