# src/ai/story_generator.py
from gemini_direct import GeminiAPI
import asyncio
import time

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
            
            if isinstance(response, str) and response.startswith('Error'):
                print(f"Error occurred: {response}")
                return None
                
            return response

        except Exception as e:
            print(f"Error generating story: {str(e)}")
            return None

    def complete_story(self, current_story):
        try:
            completion_prompt = f"""
            Complete this story with a satisfying ending:
            {current_story}
            """
            
            response = self.gemini.generate_content(
                completion_prompt,
                max_tokens=1024,
                temperature=0.7
            )
            
            if isinstance(response, str) and response.startswith('Error'):
                print(f"Error occurred: {response}")
                return None
                
            return response

        except Exception as e:
            print(f"Error completing story: {str(e)}")
            return None

def test_story_generator():
    generator = StoryGenerator()
    
    # Test story creation
    prompt = "A story about a young scientist who discovers something unexpected in the Amazon rainforest."
    print("\nGenerating story...")
    story = generator.create_story(prompt)
    
    if story:
        print(f"\nGenerated Story:\n{story}")
    else:
        print("Failed to generate story")

if __name__ == "__main__":
    test_story_generator()