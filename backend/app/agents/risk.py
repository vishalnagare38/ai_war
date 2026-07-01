from typing import Dict
import time


class RiskAgent:

    def analyze(
        self,
        transcript: str,
        ml_probability: float = 0.0,
    ) -> Dict[str, object]:

        start = time.perf_counter()

        text = transcript.lower()

        insights = []
        recommendations = []

        rule_score = 0

        # ==========================================
        # Dependency Risk
        # ==========================================

        if any(
            keyword in text
            for keyword in [
                "api",
                "vendor",
                "integration",
                "blocked",
                "blocker",
                "dependency",
            ]
        ):

            rule_score += 25

            insights.append(
                "External API/vendor dependency is impacting system integration and delivery."
            )

            recommendations.append(
                "Work with the external vendor to stabilize the integration and monitor progress daily."
            )

        # ==========================================
        # Schedule Risk
        # ==========================================

        if any(
            keyword in text
            for keyword in [
                "delay",
                "deadline",
                "behind schedule",
                "timeline",
                "release",
            ]
        ):

            rule_score += 20

            insights.append(
                "Project schedule is at risk due to delivery timeline uncertainty."
            )

            recommendations.append(
                "Review delivery milestones, assign mitigation owners, and prepare contingency plans for schedule slippage."
            )

        # ==========================================
        # Quality / Testing Risk
        # ==========================================

        if any(
            keyword in text
            for keyword in [
                "testing",
                "regression",
                "bug",
                "defect",
                "qa",
            ]
        ):

            rule_score += 20

            insights.append(
                "Testing readiness may not be sufficient for a stable production release."
            )

            recommendations.append(
                "Complete regression testing, stabilize critical workflows, and resolve release-blocking defects before deployment."
            )

        # ==========================================
        # Budget Risk
        # ==========================================

        if any(
            keyword in text
            for keyword in [
                "budget",
                "cost",
                "spending",
                "expense",
            ]
        ):

            rule_score += 15

            insights.append(
                "Project budget requires close monitoring to avoid cost overruns."
            )

            recommendations.append(
                "Review project spending and prioritize high-value deliverables."
            )

        # ==========================================
        # Resource Risk
        # ==========================================

        if any(
            keyword in text
            for keyword in [
                "ownership",
                "owner",
                "resource",
                "frontend",
                "workload",
                "assigned",
                "allocation",
            ]
        ):

            rule_score += 10

            insights.append(
                "Resource ownership and workload distribution may affect execution."
            )

            recommendations.append(
                "Assign clear ownership for critical workstreams and rebalance team workload."
            )

        # ==========================================
        # Database / Infrastructure Risk
        # ==========================================

        if any(
            keyword in text
            for keyword in [
                "database",
                "schema",
                "migration",
                "infrastructure",
            ]
        ):

            rule_score += 10

            insights.append(
                "Infrastructure readiness should be validated before deployment."
            )

            recommendations.append(
                "Complete database validation and infrastructure readiness checks."
            )

        # ==========================================
        # Combine Rule Score + ML Score
        # ==========================================

        ml_score = ml_probability * 100

        combined_score = (
            (rule_score * 0.6)
            + (ml_score * 0.4)
        )

        combined_score = min(
            combined_score,
            100,
        )

        # ==========================================
        # Final Risk Level
        # ==========================================

        if combined_score >= 75:

            level = "high"

        elif combined_score >= 45:

            level = "medium"

        else:

            level = "low"

        # ==========================================
        # Remove duplicates
        # ==========================================

        insights = list(
            dict.fromkeys(insights)
        )

        recommendations = list(
            dict.fromkeys(recommendations)
        )

        return {

            "risk_insights": insights,

            "risk_level": level,

            "risk_recommendations": recommendations,

        }