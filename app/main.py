from fastapi import FastAPI
from app.api.endpoints import resume_endpoints  # Make sure this import path is correct

app = FastAPI()

app.include_router(resume_endpoints.router, prefix="/api/v1", tags=["resume"]) 