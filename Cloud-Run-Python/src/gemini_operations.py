# src/ai/gemini_operations.py
import os
from dotenv import load_dotenv
import requests

class GeminiOperations:
    def __init__(self, db_operations):
        load_dotenv()
        self.db = db_operations
        self.settings = self.db.get_gemini_settings()
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.headers = {'Content-Type': 'application/json'}

    def generate_story_segment(self, user_input):
        settings = self.db.get_gemini_settings()
        
        data = {
            "contents": [{
                "parts": [{
                    "text": f"{settings[1]}\n\nUser Input: {user_input}"
                }]
            }],
            "generationConfig": {
                "temperature": settings[4],
                "maxOutputTokens": settings[5]
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/gemini-pro:generateContent?key={settings[3]}",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
            
            return f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            return f"Error: {str(e)}"

    def complete_story(self, current_story):
        settings = self.db.get_gemini_settings()
        
        completion_prompt = f"Complete this story with a satisfying ending:\n{current_story}"
        
        # Similar implementation as generate_story_segment
        # but with completion-specific parameters

    def create_narrative(self, selected_stories):
        settings = self.db.get_gemini_settings()
        
        narrative_prompt = f"{settings[2]}\n\nSelected Stories:\n"
        for story in selected_stories:
            narrative_prompt += f"\n{story[1]}:\n{story[2]}\n"
        
        # Similar implementation as generate_story_segment
        # but with narrative-specific parameters