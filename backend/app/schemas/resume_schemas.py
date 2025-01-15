# Move all Pydantic models here
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class Education(BaseModel):
    institution: str = Field(..., description="Name of the educational institution")
    degree: str = Field(..., description="Degree obtained or pursuing")
    field_of_study: str = Field(..., description="Field or major of study")
    start_date: str = Field(..., description="Start date of education (YYYY-MM)")
    end_date: Optional[str] = Field(None, description="End date of education (YYYY-MM)")
    grade: Optional[str] = Field(None, description="Grade or GPA")

    class Config:
        from_attributes = True


class Experience(BaseModel):
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job title or position")
    start_date: str = Field(..., description="Start date of employment (YYYY-MM)")
    end_date: Optional[str] = Field(
        None, description="End date of employment (YYYY-MM)"
    )
    description: List[str] = Field(
        ..., description="List of job responsibilities and achievements"
    )

    class Config:
        from_attributes = True


class Skill(BaseModel):
    category: str = Field(
        ..., description="Skill category (e.g., Programming, Languages)"
    )
    skills: List[str] = Field(..., description="List of skills in this category")

    class Config:
        from_attributes = True


class ResumeCreate(BaseModel):
    full_name: str = Field(..., description="Full name of the person")
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(..., description="Contact phone number")
    summary: str = Field(..., description="Professional summary")
    education: List[Education] = Field(..., description="List of education entries")
    experience: List[Experience] = Field(
        ..., description="List of work experience entries"
    )
    skills: List[Skill] = Field(..., description="List of skill categories")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    website: Optional[str] = Field(None, description="Personal website URL")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "summary": "Experienced software engineer with 5+ years in web development",
                "education": [
                    {
                        "institution": "University of Technology",
                        "degree": "Bachelor's",
                        "field_of_study": "Computer Science",
                        "start_date": "2015-09",
                        "end_date": "2019-05",
                        "grade": "3.8 GPA",
                    }
                ],
                "experience": [
                    {
                        "company": "Tech Corp",
                        "position": "Senior Developer",
                        "start_date": "2019-06",
                        "end_date": None,
                        "description": [
                            "Led team of 5 developers",
                            "Implemented microservices architecture",
                            "Reduced system response time by 40%",
                        ],
                    }
                ],
                "skills": [
                    {
                        "category": "Programming",
                        "skills": ["Python", "JavaScript", "SQL"],
                    }
                ],
                "linkedin": "https://linkedin.com/in/johndoe",
                "github": "https://github.com/johndoe",
                "website": "https://johndoe.com",
            }
        }


class EnhancedResume(BaseModel):
    original_resume: ResumeCreate = Field(..., description="Original resume data")
    enhanced_summary: str = Field(..., description="AI-enhanced professional summary")
    skill_suggestions: List[str] = Field(
        ..., description="Suggested additional skills based on experience"
    )
    improvements: List[str] = Field(
        ..., description="Suggested improvements for the resume"
    )

    class Config:
        from_attributes = True
