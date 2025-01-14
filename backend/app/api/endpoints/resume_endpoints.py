from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from app.schemas.resume_schemas import ResumeCreate
from app.services.ai_enhancement import ResumeEnhancementService
from app.services.pdf_generator import PDFGeneratorService

router = APIRouter()
enhancement_service = ResumeEnhancementService()
pdf_service = PDFGeneratorService()

@router.get("/")
async def get_resumes():
    return {"message": "List of resumes"}

@router.post("/")
async def create_resume(resume: ResumeCreate):
    try:
        # Enhance resume using AI
        enhanced_resume = await enhancement_service.enhance_resume(resume)
        
        # Generate PDF
        pdf_filename = f"resume_{resume.full_name.replace(' ', '_').lower()}.pdf"
        pdf_path = os.path.join("temp", pdf_filename)
        
        # Ensure temp directory exists
        os.makedirs("temp", exist_ok=True)
        
        # Generate the PDF
        pdf_service.generate_pdf(resume, enhanced_resume, pdf_path)
        
        # Return both the enhanced data and the PDF
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=pdf_filename,
            headers={
                "X-Enhanced-Data": enhanced_resume.model_dump_json()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
