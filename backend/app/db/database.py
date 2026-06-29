from pymongo import MongoClient

from app.core.config import (
    MONGODB_URI,
    DATABASE_NAME,
)

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]


def get_database():
    return db


def ping_database():
    try:
        client.admin.command("ping")
        print("✅ MongoDB Connected Successfully")
        return True
    except Exception as e:
        print("❌ MongoDB Connection Failed")
        print(e)
        return False