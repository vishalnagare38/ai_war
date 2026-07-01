from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import (
    APP_NAME,
    CORS_ORIGINS,
    CORS_ORIGIN_REGEX,
)

print("CORS_ORIGINS =", CORS_ORIGINS)
print("CORS_ORIGIN_REGEX =", CORS_ORIGIN_REGEX)

app = FastAPI(title=APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Meeting War Room API is running"
    }