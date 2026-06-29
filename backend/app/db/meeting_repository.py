from datetime import datetime

from bson import ObjectId

from app.db.database import db


class MeetingRepository:

    def __init__(self):
        self.collection = db["meetings"]

    def create(self, meeting: dict):
        meeting["created_at"] = datetime.utcnow()

        result = self.collection.insert_one(meeting)

        return str(result.inserted_id)

    def get_all(self):
        meetings = list(
            self.collection.find(
                {},
                {
                    "transcript": 0,
                },
            ).sort("created_at", -1)
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
    
    def count(self):
        return self.collection.count_documents({})