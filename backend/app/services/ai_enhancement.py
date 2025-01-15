from pydantic_ai import Agent
from typing import Dict, Any
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResumeEnhancementService:
    def __init__(self):
        self.agent = Agent(
            model="openai:gpt-4o-mini",
            system_prompt="""You are an expert resume writer and career counselor with years of experience in helping 
            professionals create compelling resumes. Your task is to enhance resumes by:
            1. Improving content and impact of experience descriptions
            2. Suggesting relevant skills based on experience
            3. Providing a more compelling professional summary
            4. Offering specific suggestions for improvement
            Please maintain factual accuracy while making the content more impactful."""
        )
        logger.info("Resume Enhancement Service initialized successfully")

    async def enhance_resume(self, resume_data: Dict[Any, Any]) -> Dict[Any, Any]:
        try:
            logger.info("Attempting to call OpenAI API...")
            result = await self.agent.run(
                f"Please enhance this resume: {resume_data}"
            )
            logger.info("Successfully received API response")
            return result.data
            
        except Exception as e:
            logger.error(f"Error in AI enhancement: {str(e)}", exc_info=True)
            raise
