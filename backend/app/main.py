from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints.resume_endpoints import router as resume_router
from fastapi.openapi.utils import get_openapi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_application() -> FastAPI:
    # Log the ENABLE_SWAGGER_AUTH value
    logger.info(f"ENABLE_SWAGGER_AUTH is set to: {settings.ENABLE_SWAGGER_AUTH}")
    
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

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        # Log when OpenAPI schema is being generated
        logger.info("Generating OpenAPI schema")
        
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            description="Resume Builder API with AI-powered enhancements",
            routes=app.routes,
        )
        
        # Add security schemes only if ENABLE_SWAGGER_AUTH is True
        if settings.ENABLE_SWAGGER_AUTH:
            logger.info("Adding security schemes to OpenAPI schema")
            openapi_schema["components"]["securitySchemes"] = {
                "GoogleAuth": {
                    "type": "oauth2",
                    "flows": {
                        "authorizationCode": {
                            "authorizationUrl": "https://accounts.google.com/o/oauth2/v2/auth",
                            "tokenUrl": "https://oauth2.googleapis.com/token",
                            "refreshUrl": "https://oauth2.googleapis.com/token",
                            "scopes": {
                                "https://www.googleapis.com/auth/userinfo.email": "Access email address",
                                "https://www.googleapis.com/auth/userinfo.profile": "Access user profile"
                            }
                        }
                    }
                }
            }
            
            openapi_schema["security"] = [{"GoogleAuth": [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
            ]}]
        else:
            logger.warning("ENABLE_SWAGGER_AUTH is False, skipping security schemes")
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    @app.get("/", tags=["Health Check"])
    async def health_check():
        """
        Health check endpoint
        """
        return {"status": "healthy", "version": settings.VERSION}

    return app

app = get_application()
