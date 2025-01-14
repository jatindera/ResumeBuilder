from pydantic import BaseModel, Field
from typing import List

class ResumeContent(BaseModel):
    education: List[str] = Field(
        ...,
        description="List of educational qualifications with institution names and years"
    )
    experience: List[str] = Field(
        ...,
        description="List of work experiences with company names, roles, and key achievements"
    )
    skills: List[str] = Field(
        ...,
        description="List of technical and professional skills"
    )

class ResumeData(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone: str = Field(..., min_length=10)
    address: str = Field(..., min_length=5)
    content: ResumeContent

class ResumeRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone: str = Field(..., min_length=10)
    address: str = Field(..., min_length=5)
    description: str = Field(..., min_length=50)