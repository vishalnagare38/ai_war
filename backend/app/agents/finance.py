from typing import Dict
import time

from app.agents.schemas import FinanceAgentOutput
from app.llm.structured import call_structured_gemini


class FinanceAgent:
    def analyze(self, transcript: str) -> Dict[str, object]:
        start = time.perf_counter()

        prompt = f"""
You are the Finance Strategy Agent for an enterprise meeting analysis platform.

Analyze the meeting ONLY from a Finance and Business perspective.

Generate ONLY valid JSON.

Return:

finance_insights
- Maximum 5 insights.
- Focus on budget, forecasting, spending, financial impact and business value.

finance_risks
- Maximum 5 financial risks.
- Include only risks supported by the transcript.
- Never discuss engineering implementation.

finance_recommendations
- Maximum 5 recommendations.
- Every recommendation must mitigate a financial risk.
- Focus on:
    • budget control
    • forecasting
    • contingency planning
    • spending
    • contractor costs
    • ROI
    • business prioritization

Rules

Never recommend:

• API implementation
• Code changes
• Engineering solutions
• QA implementation
• Technical architecture

Those belong to Engineering.

Never invent facts.

Avoid duplicates.

Return ONLY valid JSON.

Transcript

{transcript}
""".strip()

        try:

            parsed = call_structured_gemini(
                prompt,
                FinanceAgentOutput,
            )
            
            if len(parsed.finance_recommendations) < 3:

                fallback = [
                    "Review budget forecasts weekly.",
                    "Prioritize high-value deliverables.",
                    "Monitor project burn rate.",
                    "Prepare contingency budget scenarios.",
                    "Reduce unnecessary spending.",
                ]

                existing = set(parsed.finance_recommendations)

                for item in fallback:
                    if len(parsed.finance_recommendations) >= 5:
                        break
                    if item not in existing:
                        parsed.finance_recommendations.append(item)

        except Exception as e:

            print(f"Finance Agent failed: {e}")

            return {

                "finance_insights": [],

                "finance_risks": [],

                "finance_recommendations": [],

                "agent_used": "FinanceAgent-Fallback",

            }

        return {
            **parsed.model_dump(),
            "agent_used": "FinanceAgent-LLM",
        }