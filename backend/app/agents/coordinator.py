from typing import Dict

from app.agents.schemas import CoordinatorAgentOutput
from app.llm.structured import call_structured_gemini


class CoordinatorAgent:
    def analyze(self, state: Dict[str, object]) -> Dict[str, object]:
        prompt = f"""
You are the Coordinator Agent in a multi-agent meeting analysis system.

You receive:

1. Product Analysis
2. Engineering Analysis
3. Finance Analysis
4. Risk Analysis
5. Machine Learning Risk Prediction
6. Consensus Score

Important fields:

- risk_level
- ml_risk_label
- ml_risk_probability
- consensus_score
- agent_agreement

Create a concise executive report.

Return:

- executive_summary
- final_decision
- priority_actions
- overall_risk_level
- coordinator_notes

Rules:

- Use all agent outputs.
- Use ML prediction in reasoning.
- Use consensus score in reasoning.
- Do not hallucinate.
- Be concise.

Current state:

{state}
""".strip()

        parsed = call_structured_gemini(prompt, CoordinatorAgentOutput)

        return {
            **parsed.model_dump(),
            "agent_used": "CoordinatorAgent-LLM",
        }