import re
from typing import Dict, List


class ProductAgent:
    """
    Product Agent v2:
    - Creates a more natural summary
    - Extracts action items
    - Detects product/business risks
    - Produces practical recommendations
    """

    def _split_sentences(self, text: str) -> List[str]:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def _extract_action_items(self, sentences: List[str]) -> List[str]:
        triggers = [
            "need to",
            "should",
            "must",
            "let's",
            "follow up",
            "assign",
            "action item",
            "we will",
            "need",
            "plan to",
            "decide",
        ]

        items = []
        for sentence in sentences:
            lower = sentence.lower()
            if any(trigger in lower for trigger in triggers):
                items.append(sentence)

        return items[:5]

    def _extract_risks(self, transcript: str) -> List[str]:
        lower = transcript.lower()
        risks = []

        keyword_map = {
            "delay": "Possible delivery delay mentioned in the meeting.",
            "deadline": "Deadline pressure detected.",
            "scope creep": "Scope creep risk identified.",
            "blocked": "A blocker or dependency may slow execution.",
            "budget": "Budget constraint may affect implementation.",
            "bug": "Quality or bug-related concern present.",
            "risk": "A direct risk was discussed.",
            "uncertain": "Uncertainty in planning or execution was mentioned.",
            "conflict": "A possible coordination conflict was detected.",
        }

        for keyword, risk in keyword_map.items():
            if keyword in lower and risk not in risks:
                risks.append(risk)

        return risks[:5]

    def _extract_summary(self, sentences: List[str]) -> str:
        if not sentences:
            return "The meeting transcript was too short to generate a meaningful summary."

        if len(sentences) == 1:
            return sentences[0]

        return f"The discussion focused on: {sentences[0]} {sentences[1]}"

    def _generate_recommendations(self, risks: List[str], action_items: List[str]) -> List[str]:
        recommendations = []

        if risks:
            recommendations.append("Prioritize the highest-risk items first.")
            recommendations.append("Break the work into smaller milestones to reduce delivery risk.")
        else:
            recommendations.append("The meeting looks stable; keep the plan focused and measurable.")

        if action_items:
            recommendations.append("Convert the action items into owners and deadlines.")
        else:
            recommendations.append("Add clear action items before the next meeting.")

        return recommendations[:5]

    def analyze(self, transcript: str) -> Dict[str, object]:
        transcript = transcript.strip()
        sentences = self._split_sentences(transcript)

        action_items = self._extract_action_items(sentences)
        risks = self._extract_risks(transcript)
        recommendations = self._generate_recommendations(risks, action_items)
        summary = self._extract_summary(sentences)

        confidence_score = 0.55
        word_count = len(transcript.split())
        if word_count > 100:
            confidence_score = 0.7
        if word_count > 250:
            confidence_score = 0.8

        return {
            "summary": summary,
            "action_items": action_items if action_items else ["No explicit action item detected."],
            "risks": risks if risks else ["No major risk detected by heuristic analysis."],
            "recommendations": recommendations,
            "confidence_score": confidence_score,
            "agent_used": "ProductAgent-v2",
        }