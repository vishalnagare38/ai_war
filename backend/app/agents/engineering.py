from typing import Dict
import time

from app.agents.schemas import EngineeringAgentOutput
from app.llm.structured import call_structured_gemini


class EngineeringAgent:
    def analyze(self, transcript: str) -> Dict[str, object]:
        start = time.perf_counter()

        prompt = f"""
You are the Engineering Lead Agent for an enterprise meeting analysis platform.

Analyze the meeting ONLY from an Engineering perspective.

Generate ONLY valid JSON.

Return:

engineering_insights
- Maximum 5 insights.
- Focus on architecture, APIs, infrastructure, deployment, testing and technical execution.

engineering_risks
- Maximum 5 technical risks.
- Include only risks explicitly supported by the transcript.
- Avoid business or financial risks.

engineering_recommendations
- Maximum 5 recommendations.
- Every recommendation must directly mitigate one engineering risk.

Focus on:

• API stability
• Backend services
• System architecture
• Infrastructure readiness
• Testing
• Deployment
• Performance
• Scalability
• Reliability

Never discuss:

• Budget
• Cost
• Spending
• ROI
• Forecasting
• Business prioritization
• Financial planning

Those belong to Finance.

Rules

Never invent facts.

Avoid duplicate ideas.

Recommendations must be technical.

Return ONLY valid JSON.

Transcript

{transcript}
""".strip()

        try:

            parsed = call_structured_gemini(
                prompt,
                EngineeringAgentOutput,
            )
            
            if len(parsed.engineering_recommendations) < 3:

                fallback = [
                    "Stabilize external API integrations.",
                    "Freeze API contracts before regression testing.",
                    "Increase automated testing coverage.",
                    "Monitor deployment readiness daily.",
                    "Resolve critical engineering blockers.",
                ]

                existing = set(parsed.engineering_recommendations)

                for item in fallback:
                    if len(parsed.engineering_recommendations) >= 5:
                        break
                    if item not in existing:
                        parsed.engineering_recommendations.append(item)

        except Exception as e:

            print(f"Engineering Agent failed: {e}")

            return {

                "engineering_insights": [],

                "engineering_risks": [],

                "engineering_recommendations": [],

                "agent_used": "EngineeringAgent-Fallback",

            }

        return {
            **parsed.model_dump(),
            "agent_used": "EngineeringAgent-LLM",
        }