from typing import Dict
import time

from app.agents.schemas import CoordinatorAgentOutput
from app.llm.structured import call_structured_gemini


class CoordinatorAgent:

    def analyze(self, state: Dict[str, object]) -> Dict[str, object]:

        start = time.perf_counter()

        prompt = f"""
You are the Executive Coordinator for an Enterprise AI Meeting War Room.

Your responsibility is to synthesize the outputs of all specialist agents into
a concise executive report suitable for senior leadership.

==================================================
PRODUCT AGENT
==================================================

Summary:
{state.get("summary")}

Risks:
{state.get("risks", [])}

Recommendations:
{state.get("recommendations", [])}


==================================================
ENGINEERING AGENT
==================================================

Insights:
{state.get("engineering_insights", [])}

Risks:
{state.get("engineering_risks", [])}

Recommendations:
{state.get("engineering_recommendations", [])}


==================================================
FINANCE AGENT
==================================================

Insights:
{state.get("finance_insights", [])}

Risks:
{state.get("finance_risks", [])}

Recommendations:
{state.get("finance_recommendations", [])}


==================================================
RISK AGENT
==================================================

Risk Level:
{state.get("risk_level")}

Insights:
{state.get("risk_insights", [])}

Recommendations:
{state.get("risk_recommendations", [])}


==================================================
ML PREDICTION
==================================================

Probability:
{state.get("ml_risk_probability")}

Risk Label:
{state.get("ml_risk_label")}

Delay Likelihood:
{state.get("delay_likelihood")}


==================================================
CONSENSUS ENGINE
==================================================

Consensus Score:
{state.get("consensus_score")}

Agreement:
{state.get("agent_agreement")}

Consensus Reason:
{state.get("consensus_reason")}

Consensus Factors:
{state.get("consensus_factors", [])}


==================================================
MEETING HEALTH
==================================================

Health Score:
{state.get("meeting_health_score")}/100

Health Label:
{state.get("meeting_health_label")}


==================================================
SYSTEM METRICS
==================================================

Processing Timeline:
{state.get("agent_timings", {})}


==================================================

YOUR TASK

Generate ONLY the following JSON fields.

1. executive_summary
- 4–6 executive sentences
- Mention biggest blocker
- Mention ML prediction
- Mention consensus
- Mention meeting health
- Mention overall business impact

2. final_decision
- One concise executive decision.

3. priority_actions
- 4–6 actions
- Highest priority first
- No duplicates

4. overall_risk_level
Must be one of:
low
medium
high

5. coordinator_notes

Write 4 concise notes.

They should explain:

• Why consensus is high/medium/low.

• Whether ML agrees with the specialist agents.

• Explain Meeting Health.

• Mention the biggest blocker.

Rules

Never invent facts.

Never contradict any agent.

Do not repeat every recommendation.

Keep the language executive-level.

Return ONLY valid JSON.
"""

        parsed = call_structured_gemini(
            prompt=prompt,
            schema=CoordinatorAgentOutput,
        )
        print(state.get("consensus_reason"))

        timings = dict(state.get("agent_timings", {}))

        timings["Coordinator Agent"] = round(
            time.perf_counter() - start,
            2,
        )

        return {
            **parsed.model_dump(),
            "agent_used": "CoordinatorAgent-LLM",
            "agent_timings": timings,
        }