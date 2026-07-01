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

        "API Integration Delay": [
            "api",
            "integration",
            "vendor",
            "blocked",
            "dependency",
            "latency",
        ],

        "Testing Coverage": [
            "testing",
            "test",
            "qa",
            "regression",
            "coverage",
            "bug",
            "defect",
        ],

        "Budget Pressure": [
            "budget",
            "cost",
            "forecast",
            "expense",
            "spending",
            "overrun",
        ],

        "Timeline Risk": [
            "deadline",
            "delay",
            "schedule",
            "timeline",
            "release",
            "launch",
            "milestone",
        ],

        "Resource Allocation": [
            "owner",
            "ownership",
            "assign",
            "resource",
            "allocation",
            "frontend",
            "engineer",
        ],

        "Database Changes": [
            "database",
            "schema",
            "migration",
        ],

        "Performance Optimization": [
            "performance",
            "optimization",
            "latency",
            "slow",
            "response time",
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

                f"{theme} was independently highlighted by "

                f"{', '.join(matched)} teams."

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

    penalty += round(ml_probability * 20)

    penalty += round((1-consensus_score) * 18)

    if any("API" in x for x in factors):
        penalty += 6

    if any("Testing" in x for x in factors):
        penalty += 5

    if any("Budget" in x for x in factors):
        penalty += 6

    if any("Timeline" in x for x in factors):
        penalty += 5

    score = max(0, min(100, 100 - penalty))

    if score >= 90:

        label = "Excellent"

    elif score >= 75:

        label = "Healthy"

    elif score >= 60:

        label = "Stable"

    elif score >= 40:

        label = "Needs Attention"

    elif score >= 20:

        label = "At Risk"

    else:

        label = "Critical"

    return score, label


def consensus_node(state: Dict[str, object]) -> Dict[str, object]:

    start = time.perf_counter()

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

    consensus_score = 1.0 - (spread * 1.35)

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

            f"The specialist agents reached strong agreement "

            f"because {len(consensus_factors)} recurring project "

            f"themes were independently identified. "

            f"The ML model also indicates a "

            f"{ml_score*100:.0f}% predicted delivery risk, "

            f"which is consistent with the specialist assessments."

        )

    elif agreement == "medium":

        consensus_reason = (

            "Most specialist agents agreed on the major "

            "delivery risks, although there were moderate "

            "differences in prioritization and recommended "

            "mitigation strategies."

        )

    else:

        consensus_reason = (

            "Specialist agents identified substantially "

            "different concerns, indicating that additional "

            "project clarification and alignment are required "

            "before making major delivery decisions."

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