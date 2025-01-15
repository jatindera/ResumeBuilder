from fastapi import APIRouter, HTTPException, Depends, Security
from typing import Dict, Any
from app.services.ai_enhancement import ResumeEnhancementService
from app.schemas.resume_schemas import ResumeCreate, ResumeResponse
from app.core.auth import get_current_user, verify_token_manually
from app.models.resume_models import Resume
from app.models.user import User

router = APIRouter()

# Protected endpoint (requires authentication)
@router.post("/enhance", response_model=Dict[str, Any])
async def enhance_resume(
    resume: ResumeCreate,
    current_user: User = Security(get_current_user)
):
    """
    Enhance a resume using AI
    """
    try:
        service = ResumeEnhancementService()
        enhanced_resume = await service.enhance_resume(resume.model_dump())
        return enhanced_resume
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error enhancing resume: {str(e)}"
        )

# Protected endpoint (requires authentication)
@router.get("/test-private")
async def test_private_endpoint(
    current_user: User = Security(get_current_user)
):
    """
    Test endpoint to verify router is working (requires auth)
    """
    return {
        "message": "Private resume endpoint is working",
        "user": current_user.email if current_user else None
    }

# Unprotected test endpoint for development
@router.get("/test-public")
async def test_public_endpoint():
    """
    Public test endpoint for development (no auth required)
    """
    return {
        "message": "Public resume endpoint is working",
        "note": "This endpoint is for testing only"
    }

@router.post("/verify-token")
async def verify_token(token: str):
    """
    Test endpoint to verify token manually
    """
    return await verify_token_manually(token)
