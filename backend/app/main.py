from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.v1.endpoints import meeting, document, scheduling, translation

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(meeting.router, prefix=settings.API_V1_STR + "/meeting", tags=["meeting"])
app.include_router(document.router, prefix=settings.API_V1_STR + "/document", tags=["document"])
app.include_router(scheduling.router, prefix=settings.API_V1_STR + "/scheduling", tags=["scheduling"])
app.include_router(translation.router, prefix=settings.API_V1_STR + "/translation", tags=["translation"])

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Office Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
