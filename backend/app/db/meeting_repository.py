from datetime import datetime

from bson import ObjectId

from app.db.database import db


class MeetingRepository:

    def __init__(self):
        self.collection = db["meetings"]

        # Create indexes (safe to call multiple times)
        self.collection.create_index("meeting_id", unique=True)
        self.collection.create_index("created_at")

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, meeting: dict):

        meeting["created_at"] = datetime.utcnow()

        result = self.collection.insert_one(meeting)

        return str(result.inserted_id)

    # =====================================================
    # READ
    # =====================================================

    def get_all(self):

        meetings = list(
            self.collection.find(
                {},
                {
                    "transcript": 0,
                },
            ).sort(
                "created_at",
                -1,
            )
        )

        for meeting in meetings:
            meeting["_id"] = str(meeting["_id"])

        return meetings

    def get_recent(self, limit: int = 5):

        meetings = list(
            self.collection.find().sort(
                "created_at",
                -1,
            ).limit(limit)
        )

        for meeting in meetings:
            meeting["_id"] = str(meeting["_id"])

        return meetings

    def get_by_id(self, mongo_id: str):

        meeting = self.collection.find_one(
            {
                "_id": ObjectId(mongo_id)
            }
        )

        if meeting:
            meeting["_id"] = str(meeting["_id"])

        return meeting

    def get_by_meeting_id(self, meeting_id: str):

        meeting = self.collection.find_one(
            {
                "meeting_id": meeting_id
            }
        )

        if meeting:
            meeting["_id"] = str(meeting["_id"])

        return meeting

    # =====================================================
    # DELETE
    # =====================================================

    def delete(self, mongo_id: str):

        result = self.collection.delete_one(
            {
                "_id": ObjectId(mongo_id)
            }
        )

        return result.deleted_count > 0

    def delete_by_meeting_id(self, meeting_id: str):

        result = self.collection.delete_one(
            {
                "meeting_id": meeting_id
            }
        )

        return result.deleted_count > 0

    # =====================================================
    # STATS
    # =====================================================

    def count(self):

        return self.collection.count_documents({})

    def dashboard_stats(self):

        meetings = list(self.collection.find())

        total = len(meetings)

        if total == 0:

            return {
                "total_meetings": 0,
                "average_health": 0,
                "average_risk_probability": 0,
                "high_risk_meetings": 0,
                "healthy_meetings": 0,
            }

        avg_health = round(
            sum(
                m.get(
                    "meeting_health_score",
                    0,
                )
                for m in meetings
            ) / total
        )

        avg_risk = round(
            sum(
                m.get(
                    "ml_risk_probability",
                    0,
                )
                for m in meetings
            ) / total,
            2,
        )

        high_risk = sum(
            1
            for m in meetings
            if m.get("overall_risk_level", "").lower() == "high"
        )

        healthy = sum(
            1
            for m in meetings
            if m.get("meeting_health_score", 0) >= 80
        )

        return {

            "total_meetings": total,

            "average_health": avg_health,

            "average_risk_probability": avg_risk,

            "high_risk_meetings": high_risk,

            "healthy_meetings": healthy,

        }