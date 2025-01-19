# src/utils/gemini_utils.py
import os
from dotenv import load_dotenv
import requests

class GeminiAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.headers = {'Content-Type': 'application/json'}

    def generate_content(self, prompt, max_tokens=100, temperature=0.7):
        url = f"{self.base_url}/gemini-pro:generateContent"
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }

        try:
            response = requests.post(
                f"{url}?key={self.api_key}",
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