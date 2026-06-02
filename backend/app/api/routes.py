from fastapi import APIRouter, HTTPException
from app.schemas import TranscriptAnalyzeRequest, AnalyzeResponse
from app.graph.workflow import build_workflow
import time

router = APIRouter(prefix="/api", tags=["Meeting War Room"])

workflow = build_workflow()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "meeting-war-room-api"
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_meeting(request: TranscriptAnalyzeRequest):
    transcript = request.transcript.strip()

    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    initial_state = {
        "meeting_title": request.meeting_title,
        "transcript": transcript,
    }

    start_time = time.time()

    result = workflow.invoke(initial_state)

    processing_time = round(
        time.time() - start_time,
        2,
    )

    result["processing_time_seconds"] = processing_time

    return AnalyzeResponse(
        meeting_title=request.meeting_title,
        summary=result.get("summary", ""),
        action_items=result.get("action_items", []),
        risks=result.get("risks", []),
        recommendations=result.get("recommendations", []),
        confidence_score=result.get("confidence_score", 0.0),
        agent_used=result.get("agent_used", "unknown"),

        engineering_insights=result.get("engineering_insights", []),
        engineering_risks=result.get("engineering_risks", []),
        engineering_recommendations=result.get("engineering_recommendations", []),

        finance_insights=result.get("finance_insights", []),
        finance_risks=result.get("finance_risks", []),
        finance_recommendations=result.get("finance_recommendations", []),

        risk_insights=result.get("risk_insights", []),
        risk_level=result.get("risk_level", "low"),
        risk_recommendations=result.get("risk_recommendations", []),

        ml_risk_probability=result.get("ml_risk_probability", 0.0),
        ml_risk_label=result.get("ml_risk_label", "low"),
        delay_likelihood=result.get("delay_likelihood", 0.0),
        consensus_score=result.get("consensus_score", 0.0),
        agent_agreement=result.get("agent_agreement", "low"),

        executive_summary=result.get("executive_summary", ""),
        final_decision=result.get("final_decision", ""),
        priority_actions=result.get("priority_actions", []),
        overall_risk_level=result.get("overall_risk_level", "low"),
        coordinator_notes=result.get("coordinator_notes", []),
        processing_time_seconds=result.get(
            "processing_time_seconds",
            0.0,
        ),
    )