def _risk_list_to_score(risks):
    count = len(risks or [])
    if count == 0:
        return 0.20
    if count == 1:
        return 0.55
    if count == 2:
        return 0.75
    return 0.90


def _label_to_score(label: str):
    mapping = {
        "low": 0.25,
        "medium": 0.60,
        "high": 0.90,
    }
    return mapping.get(str(label).lower(), 0.25)


def consensus_node(state):
    product_score = _risk_list_to_score(state.get("risks", []))
    engineering_score = _risk_list_to_score(state.get("engineering_risks", []))
    finance_score = _risk_list_to_score(state.get("finance_risks", []))
    risk_score = _label_to_score(state.get("risk_level", "low"))
    ml_score = _label_to_score(state.get("ml_risk_label", "low"))

    raw_consensus = (
        product_score
        + engineering_score
        + finance_score
        + risk_score
        + ml_score
    ) / 5.0

    # Cap it so it never becomes a suspicious 100%
    consensus = round(min(raw_consensus, 0.95), 2)

    if consensus >= 0.75:
        agreement = "high"
    elif consensus >= 0.40:
        agreement = "medium"
    else:
        agreement = "low"

    return {
        **state,
        "consensus_score": consensus,
        "agent_agreement": agreement,
    }