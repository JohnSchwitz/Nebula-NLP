# utils.py
import psycopg2
import os
from dotenv import load_dotenv
from fpdf import FPDF
import textwrap
import requests

class DatabaseOperations:
    def __init__(self, config=None):
        if config:
            self.config = config
        else:
            load_dotenv()
            self.config = {
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT'),
                'database': os.getenv('DB_NAME'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD')
            }

    def get_connection(self):
        return psycopg2.connect(**self.config)

    def get_settings(self, version_number=1): # Correct name, single settings method
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT api_key, temperature, max_tokens, story_instructions, narrative_instructions, version_number
                    FROM gemini_settings  
                    WHERE version_number = %s;
                    """,
                    (version_number,),
                )
                print("Query executed successfully.")
                row = cur.fetchone()
                if row:
                    print("Settings found.")
                    # Convert to dictionary with consistent key names (camelCase)
                    settings = {
                        'apiKey': row[0],
                        'temperature': row[1],
                        'maxTokens': row[2],
                        'storyInstructions': row[3],
                        'narrativeInstructions': row[4],
                        'versionNumber': row[5],
                    }
                    return settings
                else:
                    print(f"No settings found for version {version_number}")    
                    return None  # Or raise an exception or return default settings

    def save_story(self, user_id, story_name, story_content):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO wp_user_stories (user_id, story_name, story)
                    VALUES (%s, %s, %s)
                    RETURNING story_id;
                    """,
                    (user_id, story_name, story_content)
                )
                story_id = cur.fetchone()[0]
                conn.commit()  # Important: Commit the transaction
                return story_id

    def get_user_stories(self, user_id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT story_id, story_name, story
                    FROM wp_user_stories
                    WHERE user_id = %s
                    ORDER BY story_id DESC;
                    """,
                    (user_id,)
                )
                return cur.fetchall()
            
    def save_settings(self, settings): # Single save settings method
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Use parameterized query for security and correct column names
                cur.execute("""
                    INSERT INTO gemini_settings (api_key, temperature, max_tokens, story_instructions, narrative_instructions, version_number)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (version_number) DO UPDATE SET  # Upsert logic
                        api_key = EXCLUDED.api_key,
                        temperature = EXCLUDED.temperature,
                        max_tokens = EXCLUDED.max_tokens,
                        story_instructions = EXCLUDED.story_instructions,
                        narrative_instructions = EXCLUDED.narrative_instructions;
                    """, (settings['apiKey'], settings['temperature'], settings['maxTokens'], settings['storyInstructions'], settings['narrativeInstructions'], settings['versionNumber'])
                )
                conn.commit()

class StoryPDF(FPDF):
    def __init__(self, story_name, story_content):
        super().__init__()
        self.story_name = story_name
        self.story_content = story_content
        self.WIDTH = 210
        self.HEIGHT = 297

def generate_story_pdf(story_name, story_content):
    pdf = StoryPDF(story_name, story_content)
    pdf.add_page()
    pdf.chapter_title(story_name)
    pdf.chapter_body(story_content)
    return pdf.output(dest='S').encode('latin-1')

def generate_narrative_pdf(narrative_name, narrative_content, source_stories):
    pdf = StoryPDF(narrative_name, narrative_content) # Use narrative name
    pdf.add_page()
    pdf.chapter_title(narrative_name) # Use narrative name

    # Source stories
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Source Stories:', 0, 1, 'L')
    pdf.set_font('Times', '', 12)
    for story in source_stories:
        pdf.cell(0, 10, f"• {story.get('name', 'N/A')} (ID: {story.get('id', 'N/A')})", 0, 1, 'L')  # Assuming name and id keys
    pdf.ln(10)

    pdf.chapter_body(narrative_content)
    return pdf.output(dest='S').encode('latin-1')

class GeminiAPI:
    def __init__(self, db_operations):
        self.db = db_operations
        self.base_url = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-pro:generateText"
        self.headers = {
            'Content-Type': 'application/json',
        }

    def generate_content(self, prompt, version_number=1, max_tokens=None, temperature=None):
        settings = self.db.get_settings(version_number)
        if settings is None:
            print(f"No settings found for version {version_number}. Using defaults.")
            settings = {
                'apiKey': None,
                'temperature': 0.7,
                'maxTokens': 1000,
            }

        api_key = settings.get('apiKey') or os.environ.get("GEMINI_API_KEY")
        print(api_key)
        if not api_key:
            raise ValueError("Gemini API key not found. Set in settings or as GEMINI_API_KEY environment variable.")

        self.headers['Authorization'] = f'Bearer {api_key}'

        max_tokens = max_tokens or int(settings.get('maxTokens', 1000))
        temperature = temperature or float(settings.get('temperature', 0.7))

        url = self.base_url
        data = {
            "prompt": {
                "text": prompt
            },
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }

        try:
            print(self.headers)
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            generated_text = response.json()['candidates'][0]['output']
            return generated_text
        except requests.exceptions.RequestException as e:
            print(f"Error during Gemini API call: {e}")
            return f"Error: {e}", 500  # Return error and 500 status code
        except (KeyError, IndexError) as e:
            print(f"Error extracting text from Gemini response: {e}, Response: {response.text}")
            return f"Error: Invalid response from Gemini API", 500

    def generate_narrative(self, selected_stories):
        # Combine the selected stories into a single prompt string
        prompt = f"Create a narrative from these stories:\n\n{selected_stories}"
        try:
            narrative = self.generate_content(prompt, max_tokens=100000)  # Use generate_content
            return {'narrative': narrative} # Correctly return the narrative
        except Exception as e: # Handle any exceptions from generate_content
            print(f"Error generating narrative: {e}")
            return {'error': str(e)}, 500  # Return an error
