from pydantic_ai import Agent
from app.schemas.resume import EnhancedResume, ResumeCreate

class ResumeEnhancementService:
    def __init__(self):
        self.agent = Agent(
            'openai:gpt-4o-mini',
            result_type=EnhancedResume,
            system_prompt="""
            You are a professional resume enhancement AI. Your task is to:
            1. Analyze the provided resume
            2. Enhance the professional summary
            3. Suggest additional relevant skills based on the experience
            4. Provide specific improvements for the resume
            Be specific, professional, and focus on making the resume more impactful.
            """
        )

    async def enhance_resume(self, resume: ResumeCreate) -> EnhancedResume:
        enhanced = await self.agent.run(
            f"Please analyze and enhance this resume: {resume.model_dump_json(indent=2)}",
        )
        return enhanced.data 