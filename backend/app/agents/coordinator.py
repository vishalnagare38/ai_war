from typing import Dict
import time

from app.agents.schemas import CoordinatorAgentOutput
from app.llm.structured import call_structured_gemini


class CoordinatorAgent:

    def analyze(self, state: Dict[str, object]) -> Dict[str, object]:

        start = time.perf_counter()

        prompt = f"""
You are the Executive Coordinator for an Enterprise AI Meeting War Room.

Your responsibility is to synthesize ALL specialist outputs into a concise executive report for senior leadership.

You also have access to historical project intelligence from previous meetings stored in MongoDB.

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
PROJECT HISTORY (MongoDB Intelligence)
==================================================

Historical Summary:
{state.get("history_summary", "")}

Recurring Blockers:
{state.get("recurring_blockers", [])}

Risk Trend:
{state.get("risk_trend", "Unknown")}

Health Trend:
{state.get("health_trend", "Unknown")}

Project Momentum:
{state.get("project_momentum", "Unknown")}

==================================================
SYSTEM METRICS
==================================================

Processing Timeline:
{state.get("agent_timings", {})}

==================================================

YOUR TASK

Generate ONLY valid JSON.

Return these fields:

1. executive_summary

Write 5-6 executive sentences.

Must include:

• Biggest blocker

• ML prediction

• Consensus

• Meeting Health

• Historical trend

• Business impact

--------------------------------------------------

2. final_decision

One concise executive decision.

Mention history if relevant.

--------------------------------------------------

3. priority_actions

Return 5-6 actions.

Highest priority first.

Avoid duplicates.

--------------------------------------------------

4. overall_risk_level

Only one of:

low

medium

high

--------------------------------------------------

5. coordinator_notes

Return exactly FOUR concise notes.

Include:

• Why consensus is high/medium/low

• Whether ML agrees with specialists

• Explain historical trend

• Mention biggest blocker

Rules

Never invent facts.

Never contradict specialist agents.

Use historical information whenever available.

Write executive-level language.

Return ONLY JSON.
"""

        parsed = call_structured_gemini(
            prompt=prompt,
            schema=CoordinatorAgentOutput,
        )

        timings = dict(
            state.get(
                "agent_timings",
                {},
            )
        )

        timings["Coordinator Agent"] = round(
            time.perf_counter() - start,
            2,
        )

        return {
            **parsed.model_dump(),
            "agent_used": "CoordinatorAgent-LLM",
            "agent_timings": timings,
        }