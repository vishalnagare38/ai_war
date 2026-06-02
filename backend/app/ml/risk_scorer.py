from dataclasses import dataclass
from typing import Dict, List

from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer


def _extract_features(transcript: str) -> Dict[str, float]:
    text = transcript.lower()

    risk_keywords = [
        "delay", "blocked", "deadline", "uncertain", "risk", "bug",
        "scope creep", "dependency", "testing", "conflict"
    ]
    finance_keywords = [
        "budget", "cost", "expense", "revenue", "roi", "pricing", "funding"
    ]
    engineering_keywords = [
        "api", "database", "frontend", "backend", "deploy", "integration", "performance", "security"
    ]
    action_keywords = [
        "need to", "should", "must", "let's", "assign", "follow up", "action item"
    ]

    def count_hits(keywords: List[str]) -> int:
        return sum(1 for keyword in keywords if keyword in text)

    word_count = len(text.split())

    return {
        "word_count": float(word_count),
        "risk_keyword_count": float(count_hits(risk_keywords)),
        "finance_keyword_count": float(count_hits(finance_keywords)),
        "engineering_keyword_count": float(count_hits(engineering_keywords)),
        "action_keyword_count": float(count_hits(action_keywords)),
        "has_delay": 1.0 if "delay" in text else 0.0,
        "has_blocker": 1.0 if "blocked" in text or "dependency" in text else 0.0,
        "has_budget_issue": 1.0 if "budget" in text or "cost" in text else 0.0,
    }


@dataclass
class RiskPrediction:
    probability: float
    label: str
    delay_likelihood: float


class RiskScorer:
    """
    Lightweight scikit-learn model for demo-ready predictive analytics.
    It is trained on a tiny synthetic dataset so the project works end-to-end
    without needing external data.
    """

    def __init__(self):
        self.vectorizer = DictVectorizer(sparse=False)
        self.model = LogisticRegression(max_iter=1000)
        self._train_model()

    def _training_data(self):
        samples = [
            ("Project is on track, no blockers, no budget issues.", 0),
            ("We will finalize the plan and assign tasks today.", 0),
            ("The meeting is mostly about small updates and improvements.", 0),
            ("There is a delay because API integration is blocked.", 1),
            ("Deadline is tight and the database schema is not ready.", 1),
            ("Budget is limited and there is a risk of scope creep.", 1),
            ("Testing is behind and dependency issues are causing concern.", 1),
            ("We need to follow up on pricing and funding before launch.", 1),
            ("The team should keep monitoring progress carefully.", 0),
            ("Frontend tasks are assigned and deployment is planned.", 0),
        ]
        X = [_extract_features(text) for text, _ in samples]
        y = [label for _, label in samples]
        return X, y

    def _train_model(self):
        X, y = self._training_data()
        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)

    def predict(self, transcript: str) -> RiskPrediction:
        features = _extract_features(transcript)
        X_vec = self.vectorizer.transform([features])

        probability = float(self.model.predict_proba(X_vec)[0][1])
        label = "high" if probability >= 0.65 else "medium" if probability >= 0.40 else "low"
        delay_likelihood = probability

        return RiskPrediction(
            probability=round(probability, 3),
            label=label,
            delay_likelihood=round(delay_likelihood, 3),
        )