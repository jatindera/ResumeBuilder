from fastapi import FastAPI
from app.core.config import get_settings
from app.api.endpoints import resume
import uvicorn

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(resume.router, prefix="/api/v1", tags=["resume"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)