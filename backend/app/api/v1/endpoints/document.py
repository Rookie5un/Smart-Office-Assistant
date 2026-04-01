from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from backend.app.services.rag_engine import rag_engine

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/ingest")
async def ingest_document(text: str):
    try:
        rag_engine.ingest_text(text)
        return {"status": "success", "message": "Document ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_document(request: QueryRequest):
    try:
        answer = rag_engine.query(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
