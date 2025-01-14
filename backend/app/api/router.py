from fastapi import APIRouter, HTTPException
from app.models.resume import ResumeRequest, ResumeData
from app.services.ai_service import AIService
from app.services.pdf_service import PDFService

router = APIRouter()
ai_service = AIService()
pdf_service = PDFService()

@router.post("/generate-resume", response_model=ResumeData)
async def generate_resume(request: ResumeRequest):
    try:
        content = await ai_service.generate_resume_content(request.description)
        return ResumeData(
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address,
            content=content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-pdf")
async def generate_pdf(data: ResumeData):
    try:
        file_path = pdf_service.create_resume(data)
        return {"message": "Resume PDF generated successfully", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))