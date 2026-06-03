import time
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.graph.workflow import build_workflow
from app.schemas import AnalyzeResponse, TranscriptAnalyzeRequest
from app.utils.file_parser import extract_transcript_text

router = APIRouter(prefix="/api", tags=["Meeting War Room"])
workflow = build_workflow()


def build_analyze_response(meeting_title: Optional[str], result: dict) -> AnalyzeResponse:
    return AnalyzeResponse(
        meeting_title=meeting_title,
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
        processing_time_seconds=result.get("processing_time_seconds", 0.0),
        executive_summary=result.get("executive_summary", ""),
        final_decision=result.get("final_decision", ""),
        priority_actions=result.get("priority_actions", []),
        overall_risk_level=result.get("overall_risk_level", "low"),
        coordinator_notes=result.get("coordinator_notes", []),
    )


def run_workflow(meeting_title: Optional[str], transcript: str) -> dict:
    initial_state = {
        "meeting_title": meeting_title,
        "transcript": transcript,
    }

    start_time = time.time()
    result = workflow.invoke(initial_state)
    result["processing_time_seconds"] = round(time.time() - start_time, 2)
    return result


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "meeting-war-room-api",
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_meeting(request: TranscriptAnalyzeRequest):
    transcript = request.transcript.strip()

    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    result = run_workflow(request.meeting_title, transcript)
    return build_analyze_response(request.meeting_title, result)


@router.post("/analyze-upload", response_model=AnalyzeResponse)
async def analyze_meeting_upload(
    meeting_title: Optional[str] = Form(None),
    file: UploadFile = File(...),
):
    transcript = await extract_transcript_text(file)

    if not transcript.strip():
        raise HTTPException(status_code=400, detail="Uploaded file does not contain readable text.")

    result = run_workflow(meeting_title, transcript)
    return build_analyze_response(meeting_title, result)