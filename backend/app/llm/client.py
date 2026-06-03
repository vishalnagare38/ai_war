import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

# Debug (optional)
key = os.getenv("GEMINI_API_KEY")

@lru_cache
def get_gemini_client() -> genai.Client:
    """
    Returns cached Gemini client.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from environment."
        )

    return genai.Client(api_key=api_key)


def get_gemini_model() -> str:
    """
    Returns Gemini model from environment.
    Defaults to Gemini 2.5 Flash.
    """

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    return model