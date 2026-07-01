from typing import Dict
import time

from app.agents.product_schema import ProductAgentOutput
from app.llm.structured import call_structured_gemini


class ProductAgent:
    def analyze(self, transcript: str) -> Dict[str, object]:
        start = time.perf_counter()

        prompt = f"""
You are the Senior Product Manager Agent for an enterprise meeting analysis platform.

Analyze the meeting ONLY from a Product Management perspective.

Generate ONLY valid JSON.

Return:

summary
- 3-4 concise executive sentences.

action_items
- Exactly 5 actions.
- Begin each with a verb.
- Ordered by priority.

risks
- Maximum 5 product or delivery risks.
- Include only risks supported by the transcript.

recommendations
- Maximum 5 recommendations.
- Every recommendation must mitigate one product risk.

Focus on:

• Product roadmap
• Feature scope
• Release readiness
• Customer impact
• Delivery planning
• Prioritization
• Stakeholder alignment

Never discuss:

• Budget forecasting
• Financial planning
• Engineering implementation
• Infrastructure
• Database design

Those belong to other specialist agents.

Rules

Never hallucinate.

Avoid duplicate ideas.

Keep recommendations product-focused.

Return ONLY valid JSON.

Transcript

{transcript}
""".strip()

        try:

            parsed = call_structured_gemini(
                prompt,
                ProductAgentOutput,
            )
            
            if len(parsed.recommendations) < 3:

                fallback = [
                    "Prioritize customer-facing functionality for the next release.",
                    "Reduce delivery risks before production deployment.",
                    "Review release readiness with all stakeholders.",
                    "Track critical dependencies daily.",
                    "Freeze scope until release stabilization.",
                ]

                existing = set(parsed.recommendations)

                for item in fallback:
                    if len(parsed.recommendations) >= 5:
                        break
                    if item not in existing:
                        parsed.recommendations.append(item)

        except Exception as e:

            print(f"Product Agent failed: {e}")

            return {

                "summary":
                    "Product analysis could not be generated.",

                "action_items": [],

                "risks": [],

                "recommendations": [],

                "confidence_score": 0.0,

                "agent_used": "ProductAgent-Fallback",

            }

        return {
            "summary": parsed.summary,
            "action_items": parsed.action_items,
            "risks": parsed.risks,
            "recommendations": parsed.recommendations,
            "confidence_score": parsed.confidence_score,
            "agent_used": "ProductAgent-LLM",
        }