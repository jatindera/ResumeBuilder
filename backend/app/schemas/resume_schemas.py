from pydantic import BaseModel
from typing import Dict, Any, Optional

class ResumeBase(BaseModel):
    content: Dict[str, Any]

class ResumeCreate(ResumeBase):
    pass

class ResumeResponse(ResumeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
