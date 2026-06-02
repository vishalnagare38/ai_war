from typing import Dict, List


class FinanceAgent:
    """
    Finance Agent:
    Looks for budget, cost, revenue, ROI, and financial planning signals.
    """

    def _find_signals(self, transcript: str) -> List[str]:
        lower = transcript.lower()

        signals = []
        signal_map = {
            "budget": "Budget discussion detected.",
            "cost": "Cost impact may need review.",
            "revenue": "Revenue-related discussion detected.",
            "roi": "ROI or business value consideration is present.",
            "expense": "Expense planning may be required.",
            "pricing": "Pricing decision is involved.",
            "finance": "A finance-related topic was mentioned.",
            "funding": "Funding concern or budget support may be needed.",
            "profit": "Profit impact may be relevant.",
            "investment": "Investment consideration is present.",
        }

        for keyword, signal in signal_map.items():
            if keyword in lower and signal not in signals:
                signals.append(signal)

        return signals[:6]

    def _extract_risks(self, transcript: str) -> List[str]:
        lower = transcript.lower()

        risks = []
        risk_map = {
            "budget": "Budget may be insufficient for the planned scope.",
            "cost": "Implementation cost may exceed expectations.",
            "pricing": "Pricing strategy may need validation.",
            "funding": "Funding or resource support may be limited.",
            "revenue": "Revenue assumptions may be too optimistic.",
            "profit": "Profit impact should be checked carefully.",
        }

        for keyword, risk in risk_map.items():
            if keyword in lower and risk not in risks:
                risks.append(risk)

        return risks[:5]

    def _generate_recommendations(self, signals: List[str], risks: List[str]) -> List[str]:
        recs = []

        if signals:
            recs.append("Estimate budget and expected cost before execution.")
            recs.append("Validate the business value or ROI of the proposal.")
        else:
            recs.append("Finance impact seems minimal, but still track execution cost.")

        if risks:
            recs.append("Create a simple cost-risk checklist before approval.")
            recs.append("Review pricing and budget assumptions early.")

        return recs[:5]

    def analyze(self, transcript: str) -> Dict[str, object]:
        transcript = transcript.strip()

        finance_insights = self._find_signals(transcript)
        finance_risks = self._extract_risks(transcript)
        finance_recommendations = self._generate_recommendations(finance_insights, finance_risks)

        return {
            "finance_insights": finance_insights if finance_insights else ["No major finance signal detected."],
            "finance_risks": finance_risks if finance_risks else ["No major finance risk detected."],
            "finance_recommendations": finance_recommendations,
        }