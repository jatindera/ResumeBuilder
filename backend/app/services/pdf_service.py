from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from app.models.resume import ResumeData
import os

class PDFService:
    @staticmethod
    def create_resume(user_data: ResumeData, output_dir: str = "output") -> str:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"resume_{user_data.name.replace(' ', '_')}.pdf")
        
        c = canvas.Canvas(file_path, pagesize=letter)
        
        # Header section
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, user_data.name)
        # ... rest of the PDF generation code ...
        
        c.save()
        return file_path