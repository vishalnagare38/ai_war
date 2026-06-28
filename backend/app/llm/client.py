import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai

load_dotenv()


@lru_cache
def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from environment."
        )

    return genai.Client(api_key=api_key)


def get_gemini_model() -> str:
    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    print(f"USING GEMINI MODEL: {model}")

    return model