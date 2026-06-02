import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Meeting War Room API")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]