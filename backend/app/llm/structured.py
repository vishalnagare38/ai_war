from typing import Type, TypeVar

from pydantic import BaseModel

from app.llm.client import get_gemini_client, get_gemini_model

T = TypeVar("T", bound=BaseModel)


def call_structured_gemini(prompt: str, schema: Type[T]) -> T:
    client = get_gemini_client()
    model = get_gemini_model()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": schema,
            "temperature": 0.2,
        },
    )

    if hasattr(response, "parsed") and response.parsed:
        return response.parsed

    return schema.model_validate_json(response.text)