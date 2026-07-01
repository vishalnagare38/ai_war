from typing import Dict
import time

from app.agents.schemas import CoordinatorAgentOutput
from app.llm.structured import call_structured_gemini

from app.services.deduplicator import Deduplicator

class CoordinatorAgent:

    def analyze(self, state: Dict[str, object]) -> Dict[str, object]:

        start = time.perf_counter()

        prompt = f"""
You are the Executive Coordinator of an Enterprise AI Meeting War Room.

You are the FINAL decision maker.

Your responsibility is NOT to summarize every agent.

Your responsibility is to combine evidence from:

• Product Agent
• Engineering Agent
• Finance Agent
• Risk Agent
• ML Risk Prediction
• Consensus Engine
• Historical Intelligence

into ONE executive assessment.

==================================================
PRODUCT AGENT
==================================================

Summary:
{state.get("summary")}

Action Items:
{state.get("action_items", [])}

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
ML MODEL
==================================================

Risk Probability:
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

Consensus Factors:
{state.get("consensus_factors", [])}

Consensus Reason:
{state.get("consensus_reason")}

==================================================
PROJECT HEALTH
==================================================

Meeting Health:
{state.get("meeting_health_score")}/100

Health Label:
{state.get("meeting_health_label")}

==================================================
PROJECT HISTORY
==================================================

Historical Summary:
{state.get("history_summary")}

Recurring Blockers:
{state.get("recurring_blockers", [])}

Risk Trend:
{state.get("risk_trend")}

Health Trend:
{state.get("health_trend")}

Project Momentum:
{state.get("project_momentum")}

==================================================

IMPORTANT DECISION RULES

The ML model is ONLY ONE signal.

Never make the final decision using only ML probability.

Always combine:

1. Specialist Agents

2. Consensus

3. Historical trends

4. ML prediction

If specialists identify serious delivery risks but ML predicts low probability,
explain WHY the final executive decision is still Medium or High risk.

Likewise,

if ML predicts High risk but specialists identify few issues,
explain why the project is still manageable.

Never allow the executive summary to appear contradictory.

Instead explain WHY multiple signals produce the final decision.

Historical trends must influence the decision whenever available.

Recurring blockers should increase confidence that risks are genuine.

Meeting Health should influence urgency.

==================================================

Return ONLY valid JSON.

Fields

executive_summary

Write EXACTLY six concise executive sentences.

The summary must explain:

• biggest delivery blocker

• customer/business impact

• whether the ML prediction agrees or disagrees with specialists

• why the consensus engine supports the final decision

• how historical trends influence today's assessment

• why the selected risk level is justified

Do NOT summarize each specialist separately.

Instead produce ONE executive narrative.

final_decision

Return ONE executive decision.

Maximum 30 words.

The decision must combine

• delivery readiness

• business impact

• historical intelligence

• specialist agreement

Avoid generic wording like

"Proceed carefully."

Instead write decisions such as

"Proceed only after API stabilization and regression completion."

or

"Delay release until critical integration risks are resolved."

priority_actions

Return EXACTLY six executive actions.

Rules

• Each action must combine recommendations from multiple specialist agents whenever possible.

• Do NOT copy Product, Engineering, Finance or Risk recommendations verbatim.

• Remove duplicate ideas automatically.

• Every action should represent a management decision rather than a task list.

• Highest business impact first.

• Maximum 20 words each.

• Begin every action with a strong verb.

Examples

✓ Stabilize third-party API dependencies before approving release readiness.

✓ Freeze backend interfaces and complete regression testing before deployment.

✗ Monitor API.

✗ Continue testing.

✗ Follow engineering recommendation.

overall_risk_level

Only:

low

medium

high

This MUST reflect ALL available evidence.

coordinator_notes

Return EXACTLY four concise executive notes.

Each note must explain one unique observation.

1. Why the selected risk level is justified.

2. Whether ML agrees or conflicts with specialist analysis.

3. What historical intelligence reveals.

4. The single biggest blocker preventing successful delivery.

Do NOT repeat recommendations.

Do NOT restate the executive summary.

Rules

Never hallucinate.

Never repeat sentences.

Never copy specialist recommendations.

Write concise executive language.

Executive Quality Rules

Avoid repeating the same recommendation across multiple fields.

Do not reuse specialist wording.

Combine related evidence into a single executive conclusion.

Prefer strategic decisions over operational tasks.

If multiple agents identify the same issue, describe it once using executive language.

Historical intelligence should increase confidence, not simply repeat previous blockers.

Return ONLY JSON.
"""

        try:

            parsed = call_structured_gemini(
                prompt=prompt,
                schema=CoordinatorAgentOutput,
            )

        except Exception as e:

            print(f"Coordinator Agent failed: {e}")

            return {

                "executive_summary":
                    "Executive summary could not be generated because the coordinator model was unavailable.",

                "final_decision":
                    "Manual review recommended.",

                "priority_actions": [],

                "overall_risk_level":
                    state.get(
                        "risk_level",
                        "medium",
                    ),

                "coordinator_notes": [

                    "Coordinator agent unavailable.",

                    "Fallback response generated.",

                ],

                "agent_used":
                    "CoordinatorAgent-Fallback",

                "agent_timings":
                    state.get(
                        "agent_timings",
                        {},
                    ),

            }

        timings = dict(
            state.get(
                "agent_timings",
                {},
            )
        )

        timings["Coordinator Agent"] = max(
            round(time.perf_counter() - start, 3),
            0.01,
        )

        data = parsed.model_dump()

        data["priority_actions"] = Deduplicator.unique(
            data.get("priority_actions", [])
        )

        data["coordinator_notes"] = Deduplicator.unique(
            data.get("coordinator_notes", [])
        )

        return {
            **data,
            "agent_used": "CoordinatorAgent-LLM",
            "agent_timings": timings,
        }