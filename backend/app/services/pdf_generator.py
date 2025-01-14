from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from app.schemas.resume import ResumeCreate, EnhancedResume

class PDFGeneratorService:
    @staticmethod
    def generate_pdf(resume_data: ResumeCreate, enhanced_data: EnhancedResume, output_path: str):
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Name and Contact
        story.append(Paragraph(resume_data.full_name, styles['Heading1']))
        contact_info = f"{resume_data.email} | {resume_data.phone}"
        if resume_data.linkedin:
            contact_info += f" | LinkedIn: {resume_data.linkedin}"
        story.append(Paragraph(contact_info, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Rest of the PDF generation code...
        # (Keep the existing PDF generation logic here)
        
        doc.build(story) 