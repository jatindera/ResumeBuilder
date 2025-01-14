from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.rate_limiter import RateLimiter
from app.core.config import settings
from app.api.endpoints import resume_endpoints
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=settings.CORS_HEADERS,
)

# Add rate limiter middleware
app.middleware("http")(RateLimiter())

app.include_router(resume_endpoints.router, prefix="/api/v1", tags=["resume"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)