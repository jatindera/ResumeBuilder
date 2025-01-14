from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Define the data models
class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    grade: Optional[str] = None

class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str]

class Skill(BaseModel):
    category: str
    skills: List[str]

class ResumeCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[Skill]
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

router = APIRouter()

@router.get("/")
async def get_resumes():
    return {"message": "List of resumes"}

@router.post("/")
async def create_resume(resume: ResumeCreate):
    try:
        # Here you would typically save this to a database
        return {
            "message": "Resume created successfully",
            "data": resume.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Add more endpoints as needed
