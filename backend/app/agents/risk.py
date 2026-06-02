from typing import Dict, List


class RiskAgent:
    """
    Risk Agent:
    Combines transcript-level risk signals into a high-level risk assessment.
    """

    def _find_signals(self, transcript: str) -> List[str]:
        lower = transcript.lower()

        signals = []
        signal_map = {
            "delay": "Delivery delay concern detected.",
            "blocked": "A blocker is affecting progress.",
            "deadline": "Deadline pressure is present.",
            "uncertain": "Uncertainty in planning or execution is visible.",
            "dependency": "Dependency risk detected.",
            "risk": "Risk was explicitly discussed.",
            "bug": "Bug or quality risk is present.",
            "scope creep": "Scope creep risk detected.",
            "conflict": "Coordination conflict may exist.",
            "testing": "Testing risk may increase delivery issues.",
        }

        for keyword, signal in signal_map.items():
            if keyword in lower and signal not in signals:
                signals.append(signal)

        return signals[:8]

    def _determine_risk_level(self, signals: List[str], transcript: str) -> str:
        word_count = len(transcript.split())

        if len(signals) >= 5 or word_count > 250:
            return "high"
        if len(signals) >= 2:
            return "medium"
        return "low"

    def _generate_recommendations(self, risk_level: str, signals: List[str]) -> List[str]:
        recs = []

        if risk_level == "high":
            recs.append("Escalate this meeting outcome and assign ownership immediately.")
            recs.append("Break the scope into smaller execution milestones.")
        elif risk_level == "medium":
            recs.append("Monitor the identified risks closely.")
            recs.append("Clarify dependencies before the next review.")
        else:
            recs.append("Risk appears manageable, but keep tracking progress.")

        if signals:
            recs.append("Create a mitigation plan for each major risk signal.")

        return recs[:5]

    def analyze(self, transcript: str) -> Dict[str, object]:
        transcript = transcript.strip()

        risk_insights = self._find_signals(transcript)
        risk_level = self._determine_risk_level(risk_insights, transcript)
        risk_recommendations = self._generate_recommendations(risk_level, risk_insights)

        return {
            "risk_insights": risk_insights if risk_insights else ["No strong risk signal detected."],
            "risk_level": risk_level,
            "risk_recommendations": risk_recommendations,
        }