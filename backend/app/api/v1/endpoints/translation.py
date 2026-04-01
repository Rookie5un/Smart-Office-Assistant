from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.services.translation_service import translation_service

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    target_lang: str = "中文"

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        return translation_service.translate(request.text, request.target_lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
