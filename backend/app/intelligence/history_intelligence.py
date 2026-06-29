from collections import Counter
from typing import Dict, List


class HistoryIntelligence:

    def analyze(
        self,
        current_meeting: Dict,
        previous_meetings: List[Dict],
    ) -> Dict:

        if not previous_meetings:
            return {
                "history_summary": "This is the first recorded meeting.",
                "recurring_blockers": [],
                "risk_trend": "unknown",
                "health_trend": "unknown",
                "project_momentum": "unknown",
            }

        blocker_counter = Counter()

        previous_health_scores = []

        previous_risk_scores = []

        keywords = {
            "API delay": [
                "api",
                "blocked",
                "blocker",
                "integration",
            ],
            "Testing": [
                "testing",
                "test",
            ],
            "Budget": [
                "budget",
                "cost",
            ],
            "Deadline": [
                "deadline",
                "delay",
            ],
            "Database": [
                "database",
                "schema",
            ],
            "Ownership": [
                "owner",
                "ownership",
                "assign",
            ],
        }

        for meeting in previous_meetings:

            text = " ".join(

                meeting.get("risks", [])

                + meeting.get("recommendations", [])

                + meeting.get("engineering_risks", [])

                + meeting.get("engineering_recommendations", [])

                + meeting.get("finance_risks", [])

                + meeting.get("finance_recommendations", [])

                + meeting.get("risk_insights", [])

            ).lower()

            for blocker, words in keywords.items():

                if any(word in text for word in words):

                    blocker_counter[blocker] += 1

            previous_health_scores.append(
                meeting.get(
                    "meeting_health_score",
                    0,
                )
            )

            previous_risk_scores.append(
                meeting.get(
                    "ml_risk_probability",
                    0,
                )
            )

        recurring = []

        for blocker, count in blocker_counter.items():

            if count >= 2:

                recurring.append(
                    f"{blocker} appeared in {count} previous meetings."
                )

        current_health = current_meeting.get(
            "meeting_health_score",
            0,
        )

        average_previous_health = (
            sum(previous_health_scores)
            / len(previous_health_scores)
        )

        if current_health > average_previous_health + 5:

            health_trend = "improving"

        elif current_health < average_previous_health - 5:

            health_trend = "declining"

        else:

            health_trend = "stable"

        current_risk = current_meeting.get(
            "ml_risk_probability",
            0,
        )

        average_previous_risk = (
            sum(previous_risk_scores)
            / len(previous_risk_scores)
        )

        if current_risk > average_previous_risk + 0.05:

            risk_trend = "increasing"

        elif current_risk < average_previous_risk - 0.05:

            risk_trend = "decreasing"

        else:

            risk_trend = "stable"

        if (
            health_trend == "improving"
            and risk_trend == "decreasing"
        ):

            momentum = "positive"

        elif (
            health_trend == "declining"
            and risk_trend == "increasing"
        ):

            momentum = "negative"

        else:

            momentum = "mixed"

        return {

            "history_summary":
                f"Compared against the last {len(previous_meetings)} meeting(s).",

            "recurring_blockers":
                recurring,

            "risk_trend":
                risk_trend,

            "health_trend":
                health_trend,

            "project_momentum":
                momentum,

        }