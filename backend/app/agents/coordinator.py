from typing import Dict, List


class CoordinatorAgent:
    """
    Coordinator Agent:
    Combines outputs from all specialist agents into one executive report.
    """

    def _dedupe(self, items: List[str]) -> List[str]:
        seen = set()
        result = []
        for item in items:
            normalized = item.strip().lower()
            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(item)
        return result

    def _overall_risk_level(self, state: Dict[str, object]) -> str:
        ml_label = str(state.get("ml_risk_label", "low")).lower()
        risk_level = str(state.get("risk_level", "low")).lower()
        engineering_risks = state.get("engineering_risks", []) or []
        finance_risks = state.get("finance_risks", []) or []
        product_risks = state.get("risks", []) or []

        total_risks = len(engineering_risks) + len(finance_risks) + len(product_risks)

        if ml_label == "high" or risk_level == "high" or total_risks >= 8:
            return "high"
        if ml_label == "medium" or risk_level == "medium" or total_risks >= 4:
            return "medium"
        return "low"

    def _final_decision(self, overall_risk_level: str) -> str:
        if overall_risk_level == "high":
            return "Pause execution until blockers and dependencies are resolved."
        if overall_risk_level == "medium":
            return "Proceed with caution and monitor risks closely."
        return "Proceed with the current plan."

    def _executive_summary(self, state: Dict[str, object], overall_risk_level: str) -> str:
        product_summary = str(state.get("summary", "No product summary available."))
        engineering_insights = state.get("engineering_insights", []) or []
        finance_insights = state.get("finance_insights", []) or []
        ml_probability = state.get("ml_risk_probability", 0.0)

        eng_part = engineering_insights[0] if engineering_insights else "No major engineering issue detected."
        fin_part = finance_insights[0] if finance_insights else "No major finance issue detected."

        return (
            f"{product_summary} "
            f"Engineering view: {eng_part} "
            f"Finance view: {fin_part} "
            f"ML predicted risk probability: {ml_probability}. "
            f"Overall risk level: {overall_risk_level}."
        )

    def _priority_actions(self, state: Dict[str, object]) -> List[str]:
        actions = []

        actions.extend(state.get("action_items", []) or [])
        actions.extend(state.get("engineering_recommendations", []) or [])
        actions.extend(state.get("finance_recommendations", []) or [])
        actions.extend(state.get("risk_recommendations", []) or [])
        actions.extend(state.get("recommendations", []) or [])

        ml_label = str(state.get("ml_risk_label", "low")).lower()
        if ml_label == "high":
            actions.append("ML model predicts high delay likelihood, so escalate the plan immediately.")
        elif ml_label == "medium":
            actions.append("ML model predicts moderate risk, so monitor the work closely.")

        cleaned = [a for a in actions if isinstance(a, str) and a.strip()]
        deduped = self._dedupe(cleaned)

        return deduped[:6]

    def analyze(self, state: Dict[str, object]) -> Dict[str, object]:
        overall_risk_level = self._overall_risk_level(state)
        final_decision = self._final_decision(overall_risk_level)
        executive_summary = self._executive_summary(state, overall_risk_level)
        priority_actions = self._priority_actions(state)

        coordinator_notes = [
            "Coordinator merged specialist agent outputs into one executive report.",
            "Final recommendation is based on product, engineering, finance, risk, and ML signals.",
        ]

        return {
            "executive_summary": executive_summary,
            "final_decision": final_decision,
            "priority_actions": priority_actions if priority_actions else ["No priority action identified."],
            "overall_risk_level": overall_risk_level,
            "coordinator_notes": coordinator_notes,
            "agent_used": "CoordinatorAgent-v2",
        }