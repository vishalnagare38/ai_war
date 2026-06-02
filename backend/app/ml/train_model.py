import json
import joblib

from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer


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


def main():
    data_file = BASE_DIR / "training_data.json"

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    X = [extract_features(row["text"]) for row in data]
    y = [row["label"] for row in data]

    vectorizer = DictVectorizer(sparse=False)

    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=1000)

    model.fit(X_vec, y)

    joblib.dump(model, BASE_DIR / "model.pkl")
    joblib.dump(vectorizer, BASE_DIR / "vectorizer.pkl")

    print("Model saved successfully")


if __name__ == "__main__":
    main()