import json
import time
from typing import Type, TypeVar

from pydantic import BaseModel
from google.genai.errors import ServerError

from app.llm.client import get_gemini_client, get_gemini_model

T = TypeVar("T", bound=BaseModel)


def call_structured_gemini(prompt: str, schema: Type[T]) -> T:
    client = get_gemini_client()
    model = get_gemini_model()

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": schema,
                    "temperature": 0.2,
                },
            )

            # Gemini parsed response
            if hasattr(response, "parsed") and response.parsed:
                return response.parsed

            text = response.text.strip()

            # Direct validation
            try:
                return schema.model_validate_json(text)
            except Exception:
                pass

            # Extract JSON if wrapped in markdown
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            return schema.model_validate(json.loads(text))

        except ServerError as e:
            last_error = e

            print(
                f"Gemini server busy. Retry {attempt + 1}/3..."
            )

            if attempt < 2:
                time.sleep(5)
                continue

            raise

        except Exception as e:
            last_error = e

            print(
                f"Gemini parse error. Retry {attempt + 1}/3..."
            )

            if attempt < 2:
                time.sleep(2)
                continue

            raise

    raise last_error