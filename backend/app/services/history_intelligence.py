from collections import Counter

from app.db.meeting_repository import MeetingRepository


class HistoryIntelligence:

    def __init__(self):
        self.repository = MeetingRepository()

    def analyze(self):

        meetings = self.repository.get_recent(5)

        if len(meetings) == 0:

            return {
                "total_meetings": 0,
                "average_health": 0,
                "average_risk_probability": 0,
                "high_risk_meetings": 0,
                "healthy_meetings": 0,
                "history_summary": "No meetings have been analyzed yet.",
                "recurring_blockers": [],
                "risk_trend": "No Data",
                "health_trend": "No Data",
                "project_momentum": "Unknown",
            }

        total = len(meetings)

        avg_health = round(
            sum(
                meeting.get(
                    "meeting_health_score",
                    0,
                )
                for meeting in meetings
            )
            / total,
            1,
        )

        avg_risk = round(
            sum(
                meeting.get(
                    "ml_risk_probability",
                    0,
                )
                for meeting in meetings
            )
            / total,
            2,
        )

        high_risk = sum(
            1
            for meeting in meetings
            if meeting.get(
                "overall_risk_level",
                "",
            ).lower()
            == "high"
        )

        healthy = sum(
            1
            for meeting in meetings
            if meeting.get(
                "meeting_health_score",
                0,
            )
            >= 75
        )

        keywords = []

        for meeting in meetings:

            for risk in meeting.get(
                "risks",
                [],
            ):

                text = risk.lower()

                if "api" in text:
                    keywords.append("API")

                if "testing" in text:
                    keywords.append("Testing")

                if "budget" in text:
                    keywords.append("Budget")

                if "database" in text:
                    keywords.append("Database")

                if "frontend" in text:
                    keywords.append("Frontend")

                if "backend" in text:
                    keywords.append("Backend")

                if "delay" in text:
                    keywords.append("Delay")

        recurring = [
            item
            for item, _
            in Counter(
                keywords
            ).most_common(5)
        ]

        latest = meetings[0]

        latest_health = latest.get(
            "meeting_health_score",
            0,
        )

        oldest_health = meetings[-1].get(
            "meeting_health_score",
            0,
        )

        if latest_health > oldest_health:

            momentum = "Positive"

        elif latest_health < oldest_health:

            momentum = "Negative"

        else:

            momentum = "Stable"

        risk_levels = [
            meeting.get(
                "overall_risk_level",
                "low",
            ).capitalize()
            for meeting in reversed(meetings)
        ]

        health_scores = [
            meeting.get(
                "meeting_health_score",
                0,
            )
            for meeting in reversed(meetings)
        ]

        history_summary = (
            f"Analysis of the last {total} meetings "
            f"shows an average health score of {avg_health}/100 "
            f"with an average ML risk probability of "
            f"{round(avg_risk*100)}%. "
            f"The most recurring blockers are "
            f"{', '.join(recurring) if recurring else 'none'}."
        )

        return {

            "total_meetings": total,

            "average_health": avg_health,

            "average_risk_probability": avg_risk,

            "high_risk_meetings": high_risk,

            "healthy_meetings": healthy,

            "history_summary": history_summary,

            "recurring_blockers": recurring,

            "risk_trend": risk_levels,

            "health_trend": health_scores,

            "project_momentum": momentum,

        }