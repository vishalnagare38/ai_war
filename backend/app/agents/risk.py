from typing import Dict
import time


class RiskAgent:
    def analyze(self, transcript: str, ml_probability: float = 0.0) -> Dict[str, object]:
        start = time.time()
        text = transcript.lower()

        insights = []
        recommendations = []

        if "blocked" in text or "blocker" in text or "api" in text:
            insights.append("Backend integration is blocked.")
            recommendations.append("Resolve blocker immediately.")

        if "delay" in text or "deadline" in text:
            insights.append("Project delay risk detected.")
            recommendations.append("Review project timeline and dependencies.")

        if "budget" in text or "cost" in text:
            insights.append("Budget concern detected.")
            recommendations.append("Implement cost-control measures.")

        if "testing" in text:
            insights.append("Testing progress may affect release timelines.")
            recommendations.append("Increase testing effort and coverage.")

        if ml_probability >= 0.75:
            level = "high"
        elif ml_probability >= 0.4:
            level = "medium"
        else:
            level = "low"

        return {
            "risk_insights": insights,
            "risk_level": level,
            "risk_recommendations": recommendations,
            "_duration": round(time.time() - start, 2),
        }