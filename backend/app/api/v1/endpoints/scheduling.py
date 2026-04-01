from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.scheduling_service import scheduling_service

router = APIRouter()

class ScheduleRequest(BaseModel):
    text: str

@router.post("/parse")
async def parse_schedule(request: ScheduleRequest):
    try:
        return scheduling_service.parse_intent(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
