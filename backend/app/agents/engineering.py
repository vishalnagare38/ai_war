import re
from typing import Dict, List


class EngineeringAgent:
    """
    Engineering Agent:
    Looks for technical risks, implementation complexity, and engineering follow-ups.
    """

    def _find_signals(self, transcript: str) -> List[str]:
        lower = transcript.lower()

        signals = []
        signal_map = {
            "api": "API integration needs attention.",
            "database": "Database design or schema work is mentioned.",
            "frontend": "Frontend work is part of the discussion.",
            "backend": "Backend work is part of the discussion.",
            "testing": "Testing requirements are present.",
            "deploy": "Deployment concerns are present.",
            "performance": "Performance optimization may be needed.",
            "security": "Security considerations are present.",
            "bug": "Bug fixing or quality issues are mentioned.",
            "integration": "System integration may be a risk area.",
            "scalability": "Scalability concerns are present.",
        }

        for keyword, signal in signal_map.items():
            if keyword in lower and signal not in signals:
                signals.append(signal)

        return signals[:6]

    def _extract_engineering_risks(self, transcript: str) -> List[str]:
        lower = transcript.lower()

        risks = []
        risk_map = {
            "api": "Unclear API contract may slow integration.",
            "database": "Database schema changes can create rework.",
            "testing": "Lack of testing may increase defects.",
            "deploy": "Deployment readiness may be delayed.",
            "performance": "Performance may become an issue later.",
            "security": "Security review may be needed before release.",
            "integration": "Integration dependency can block progress.",
        }

        for keyword, risk in risk_map.items():
            if keyword in lower and risk not in risks:
                risks.append(risk)

        return risks[:5]

    def _generate_recommendations(self, signals: List[str], risks: List[str]) -> List[str]:
        recs = []

        if signals:
            recs.append("Split the engineering work into smaller implementation tasks.")
            recs.append("Create a clear technical checklist before coding.")
        else:
            recs.append("The engineering side looks simple, keep the implementation lightweight.")

        if risks:
            recs.append("Add testing and validation early to avoid rework.")
            recs.append("Document API and schema decisions before implementation.")

        return recs[:5]

    def analyze(self, transcript: str) -> Dict[str, object]:
        transcript = transcript.strip()

        engineering_insights = self._find_signals(transcript)
        engineering_risks = self._extract_engineering_risks(transcript)
        engineering_recommendations = self._generate_recommendations(
            engineering_insights, engineering_risks
        )

        return {
            "engineering_insights": engineering_insights if engineering_insights else ["No strong engineering signal detected."],
            "engineering_risks": engineering_risks if engineering_risks else ["No major engineering risk detected."],
            "engineering_recommendations": engineering_recommendations,
        }