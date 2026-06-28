from statistics import median
from typing import Dict, List
import time


def _score_from_risk_count(count: int) -> float:
    if count <= 0:
        return 0.20
    if count == 1:
        return 0.40
    if count == 2:
        return 0.60
    if count == 3:
        return 0.75
    return 0.85


def _score_from_risk_level(level: str) -> float:
    mapping = {
        "low": 0.25,
        "medium": 0.60,
        "high": 0.90,
    }
    return mapping.get(str(level).lower(), 0.25)


def _build_theme_factors(state: Dict[str, object]) -> List[str]:
    sections = {
        "Product": " ".join(
            list(state.get("risks", []))
            + list(state.get("recommendations", []))
        ).lower(),

        "Engineering": " ".join(
            list(state.get("engineering_insights", []))
            + list(state.get("engineering_risks", []))
            + list(state.get("engineering_recommendations", []))
        ).lower(),

        "Finance": " ".join(
            list(state.get("finance_insights", []))
            + list(state.get("finance_risks", []))
            + list(state.get("finance_recommendations", []))
        ).lower(),

        "Risk": " ".join(
            list(state.get("risk_insights", []))
            + list(state.get("risk_recommendations", []))
        ).lower(),
    }

    themes = {
        "API delay / blocker": [
            "api",
            "block",
            "blocked",
            "blocker",
            "integration",
        ],
        "Testing delay": [
            "testing",
            "test",
            "behind schedule",
            "deadline",
        ],
        "Budget constraint": [
            "budget",
            "cost",
            "cost control",
            "overrun",
        ],
        "Scope finalization": [
            "mvp scope",
            "scope",
            "finalize",
            "finalization",
        ],
        "Ownership gap": [
            "ownership",
            "assign",
            "owner",
        ],
        "Database schema follow-up": [
            "schema",
            "database schema",
        ],
    }

    factors: List[str] = []

    for theme, keywords in themes.items():

        matched = []

        for section_name, text in sections.items():

            if any(keyword in text for keyword in keywords):
                matched.append(section_name)

        matched = sorted(set(matched))

        if len(matched) >= 2:
            factors.append(
                f"{theme} is consistently identified by {', '.join(matched)}."
            )

    ml_probability = float(
        state.get("ml_risk_probability", 0.0) or 0.0
    )

    if ml_probability >= 0.75:
        factors.append(
            f"ML predicts high risk with {ml_probability*100:.0f}% probability."
        )

    return factors


def _compute_meeting_health(
    ml_probability: float,
    consensus_score: float,
    factors: List[str],
):

    penalty = 0

    penalty += int(ml_probability * 25)
    penalty += int((1 - consensus_score) * 20)

    if any("API delay" in x for x in factors):
        penalty += 6

    if any("Testing delay" in x for x in factors):
        penalty += 6

    if any("Budget constraint" in x for x in factors):
        penalty += 8

    score = max(0, min(100, 100 - penalty))

    if score >= 85:
        label = "Healthy"
    elif score >= 70:
        label = "Stable"
    elif score >= 50:
        label = "Needs Attention"
    elif score >= 30:
        label = "At Risk"
    else:
        label = "Critical"

    return score, label


def consensus_node(state: Dict[str, object]) -> Dict[str, object]:

    start = time.perf_counter()

    # IMPORTANT: Fixes your NameError
    timings = dict(state.get("agent_timings", {}))

    product_score = _score_from_risk_count(
        len(state.get("risks", []))
    )

    engineering_score = _score_from_risk_count(
        len(state.get("engineering_risks", []))
    )

    finance_score = _score_from_risk_count(
        len(state.get("finance_risks", []))
    )

    risk_score = _score_from_risk_level(
        state.get("risk_level", "low")
    )

    ml_score = float(
        state.get("ml_risk_probability", 0.0) or 0.0
    )

    scores = [
        product_score,
        engineering_score,
        finance_score,
        risk_score,
        ml_score,
    ]

    med = median(scores)

    spread = (
        sum(abs(score - med) for score in scores)
        / len(scores)
    )

    consensus_score = 1.0 - (spread * 1.8)

    consensus_factors = _build_theme_factors(state)

    consensus_score += min(
        len(consensus_factors) * 0.015,
        0.06,
    )

    consensus_score = round(
        max(0.05, min(consensus_score, 0.95)),
        2,
    )

    if consensus_score >= 0.80:
        agreement = "high"
    elif consensus_score >= 0.55:
        agreement = "medium"
    else:
        agreement = "low"

    meeting_health_score, meeting_health_label = (
        _compute_meeting_health(
            ml_score,
            consensus_score,
            consensus_factors,
        )
    )

    if agreement == "high":

        consensus_reason = (
            f"High agreement was reached because "
            f"{len(consensus_factors)} common project themes "
            f"were independently identified across multiple "
            f"specialist agents. The ML model reinforces this "
            f"assessment with a predicted high-risk probability "
            f"of {ml_score*100:.0f}%."
        )

    elif agreement == "medium":

        consensus_reason = (
            "Most specialist agents agree on the major project "
            "risks, although there are some differences in "
            "their recommended actions."
        )

    else:

        consensus_reason = (
            "Specialist agents identified different project "
            "concerns, resulting in relatively low consensus."
        )

    timings["Consensus Engine"] = round(
        time.perf_counter() - start,
        2,
    )

    return {
        **state,
        "consensus_score": consensus_score,
        "agent_agreement": agreement,
        "consensus_factors": consensus_factors,
        "consensus_reason": consensus_reason,
        "meeting_health_score": meeting_health_score,
        "meeting_health_label": meeting_health_label,
        "agent_timings": timings,
    }