from pydantic_ai import Agent
from app.models.resume import ResumeContent
import json

class AIService:
    def __init__(self):
        self.agent = Agent(
            "gpt-4",
            system_prompt="""You are a professional resume writer. Generate specific and detailed entries for education, work experience, and skills based on the user's description.
            Always return the response in the following JSON format:
            {
                "education": ["entry1", "entry2", ...],
                "experience": ["entry1", "entry2", ...],
                "skills": ["skill1", "skill2", ...]
            }"""
        )

    async def generate_resume_content(self, description: str) -> ResumeContent:
        result = await self.agent.run(f"Create a professional resume content based on this description: {description}")
        
        if isinstance(result.data, str):
            content_dict = json.loads(result.data)
        else:
            content_dict = result.data
            
        return ResumeContent(**content_dict)