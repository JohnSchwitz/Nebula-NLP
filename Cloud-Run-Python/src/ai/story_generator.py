# src/ai/story_generator.py
from src.ai.gemini_direct import GeminiAPI
import logging

logger = logging.getLogger(__name__)

class StoryGenerator:
    def __init__(self):
        self.gemini = GeminiAPI()

    def create_story(self, prompt):
        try:
            story_prompt = f"""
            Create a story with the following elements:
            {prompt}
            
            Make it approximately 1000 words with:
            - Interesting characters
            - Clear setting
            - Engaging plot
            - Surprise twist
            """
            
            response = self.gemini.generate_content(
                story_prompt,
                max_tokens=2048,
                temperature=0.8
            )
            
            if response is None or (isinstance(response, str) and response.startswith('Error')):
                logger.error(f"Story generation failed: {response}")
                return None
                
            return response

        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            return None