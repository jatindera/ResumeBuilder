from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints.resume_endpoints import router as resume_router

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Resume Builder API with AI-powered enhancements",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Include routers
    app.include_router(resume_router, prefix="/resumes", tags=["Resumes"])

    @app.get("/", tags=["Health Check"])
    async def health_check():
        """
        Health check endpoint
        """
        return {"status": "healthy", "version": settings.VERSION}

    return app

app = get_application()
