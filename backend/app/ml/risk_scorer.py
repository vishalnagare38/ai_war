from dataclasses import dataclass
from pathlib import Path

import joblib


BASE_DIR = Path(__file__).parent


def extract_features(text: str):
    text = text.lower()

    risk_keywords = [
        "delay",
        "blocked",
        "deadline",
        "risk",
        "bug",
        "dependency",
        "testing",
        "scope creep",
    ]

    return {
        "word_count": len(text.split()),
        "risk_keyword_count": sum(
            1 for keyword in risk_keywords if keyword in text
        ),
        "has_delay": 1 if "delay" in text else 0,
        "has_blocker": 1 if "blocked" in text else 0,
        "has_bug": 1 if "bug" in text else 0,
    }


@dataclass
class RiskPrediction:
    probability: float
    label: str
    delay_likelihood: float


class RiskScorer:

    def __init__(self):
        self.model = joblib.load(BASE_DIR / "model.pkl")
        self.vectorizer = joblib.load(BASE_DIR / "vectorizer.pkl")

    def predict(self, transcript: str):

        features = extract_features(transcript)

        X = self.vectorizer.transform([features])

        probability = float(
            self.model.predict_proba(X)[0][1]
        )

        # avoid unrealistic 100%
        probability = max(
            0.05,
            min(probability, 0.95)
        )

        if probability >= 0.7:
            label = "high"
        elif probability >= 0.4:
            label = "medium"
        else:
            label = "low"

        return RiskPrediction(
            probability=round(probability, 3),
            label=label,
            delay_likelihood=round(probability, 3),
        )