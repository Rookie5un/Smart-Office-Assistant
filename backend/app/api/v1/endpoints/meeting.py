from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.meeting_service import meeting_service

router = APIRouter()

class TranscriptRequest(BaseModel):
    transcript: str

@router.post("/summary")
async def create_summary(request: TranscriptRequest):
    try:
        return meeting_service.generate_summary(request.transcript)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
