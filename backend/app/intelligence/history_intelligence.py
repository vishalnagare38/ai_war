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
                "history_summary": "This is the first recorded meeting. Historical trends will become available as more meetings are analyzed.",
                "recurring_blockers": [],
                "risk_trend": "No historical data",
                "health_trend": "No historical data",
                "project_momentum": "No historical data",
            }

        blocker_counter = Counter()

        previous_health_scores = []

        previous_risk_scores = []

        keywords = {

            "API Integration": [
                "api",
                "integration",
                "vendor",
                "blocked",
                "dependency",
            ],

            "Testing": [
                "testing",
                "test",
                "qa",
                "regression",
                "bug",
                "defect",
            ],

            "Budget": [
                "budget",
                "cost",
                "expense",
                "spending",
            ],

            "Timeline": [
                "deadline",
                "delay",
                "schedule",
                "release",
                "timeline",
            ],

            "Database": [
                "database",
                "schema",
                "migration",
            ],

            "Infrastructure": [
                "deployment",
                "server",
                "infrastructure",
            ],

            "Ownership": [
                "owner",
                "ownership",
                "assign",
                "resource",
                "allocation",
                "frontend",
            ],
        }

        current_text = " ".join(

            current_meeting.get("risks", [])

            + current_meeting.get("recommendations", [])

            + current_meeting.get("engineering_risks", [])

            + current_meeting.get("engineering_recommendations", [])

            + current_meeting.get("finance_risks", [])

            + current_meeting.get("finance_recommendations", [])

            + current_meeting.get("risk_insights", [])

        ).lower()
        
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


        for blocker, words in keywords.items():

            if any(word in current_text for word in words):

                blocker_counter[blocker] += 1
                
        recurring = []

        for blocker, count in blocker_counter.items():

            if count >= 2:

                recurring.append(

                    f"{blocker} has remained a recurring blocker across the last {count} meetings."

                )
        
        recurring.sort()

        current_health = current_meeting.get(
            "meeting_health_score",
            0,
        )

        average_previous_health = (

            sum(previous_health_scores)

            / max(

                len(previous_health_scores),

                1,

            )

        )

        health_difference = (
            current_health
            - average_previous_health
        )

        if health_difference >= 8:

            health_trend = "improving"

        elif health_difference <= -8:

            health_trend = "declining"

        else:

            health_trend = "stable"

        current_risk = current_meeting.get(
            "ml_risk_probability",
            0,
        )

        average_previous_risk = (

            sum(previous_risk_scores)

            / max(

                len(previous_risk_scores),

                1,

            )

        )

        risk_difference = (
            current_risk
            - average_previous_risk
        )

        if risk_difference >= 0.08:

            risk_trend = "increasing"

        elif risk_difference <= -0.08:

            risk_trend = "decreasing"

        else:

            risk_trend = "stable"

        if (
            health_trend == "improving"
            and risk_trend == "decreasing"
        ):

            momentum = "Strong Positive"

        elif (
            health_trend == "improving"
        ):

            momentum = "Improving"

        elif (
            health_trend == "declining"
            and risk_trend == "increasing"
        ):

            momentum = "Critical"

        elif (
            health_trend == "declining"
        ):

            momentum = "Declining"

        else:

            momentum = "Stable"

        recurring = recurring[:5]
        
        history_summary = (

            f"Historical analysis across the previous "
            f"{len(previous_meetings)} meeting(s) indicates "
            f"an average project health of "
            f"{round(average_previous_health)}/100 "
            f"and an average predicted delivery risk of "
            f"{round(average_previous_risk * 100)}%. "
            f"Project health is currently "
            f"{health_trend}, delivery risk is "
            f"{risk_trend}, resulting in "
            f"{momentum.lower()} project momentum."

        )

        return {

            "history_summary": history_summary,

            "recurring_blockers": recurring,

            "risk_trend": risk_trend,

            "health_trend": health_trend,

            "project_momentum": momentum,

        }