from typing import Dict
import time

from app.agents.schemas import EngineeringAgentOutput
from app.llm.structured import call_structured_gemini


class EngineeringAgent:
    def analyze(self, transcript: str) -> Dict[str, object]:
        start = time.time()

        prompt = f"""
You are the Engineering Agent in a multi-agent meeting analysis system.

Analyze the transcript from an engineering perspective and return:
- engineering_insights
- engineering_risks
- engineering_recommendations

Rules:
- Be concise and specific.
- Only use information supported by the transcript.
- Return valid JSON only.

Transcript:
{transcript}
""".strip()

        parsed = call_structured_gemini(prompt, EngineeringAgentOutput)

        return {
            **parsed.model_dump(),
            "agent_used": "EngineeringAgent-LLM",
            "_duration": round(time.time() - start, 2),
        }