# gemini_api.py
import google.ai.generativelanguage as generative_language
from google.api_core.client_options import ClientOptions
import os

API_KEY = os.environ.get("AIzaSyA8F7ne8nWDKUny1LOsaT5tFgicazBuULQ")

def create_gemini_client():
    if API_KEY:
        client_options = ClientOptions(api_key=API_KEY)
    else:
        raise ValueError("GEMINI_API_KEY must be set")
    return generative_language.GenerativeLanguageServiceClient(client_options=client_options)

def call_gemini(client, prompt, temperature=0.7, max_output_tokens=512):
    model = "models/gemini-pro"  # Or the specific model you want to use
    response = client.generate_text(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    return response.candidates[0].output # Return generated text