import re
from difflib import SequenceMatcher
from typing import List


class Deduplicator:
    """
    Removes duplicate or nearly-duplicate
    recommendations, risks and notes.
    """

    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()

        text = re.sub(r"[^\w\s]", "", text)

        text = re.sub(r"\s+", " ", text)

        return text

    @classmethod
    def unique(
        cls,
        items: List[str],
        threshold: float = 0.82,
    ) -> List[str]:

        cleaned = []

        normalized = []

        for item in items:

            if not item:
                continue

            current = cls.normalize(item)

            duplicate = False

            for existing in normalized:

                similarity = SequenceMatcher(
                    None,
                    current,
                    existing,
                ).ratio()

                if similarity >= threshold:
                    duplicate = True
                    break

            if not duplicate:

                normalized.append(current)

                cleaned.append(item.strip())

        return cleaned