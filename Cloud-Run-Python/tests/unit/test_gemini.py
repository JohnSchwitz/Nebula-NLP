# tests/unit/test_gemini.py
import pytest
from src.utils.gemini_utils import GeminiAPI

def test_gemini_connection():
    gemini = GeminiAPI()
    prompt = "Write a one-sentence test story."
    response = gemini.generate_content(prompt)
    print(f"Gemini Response: {response}")  # For debugging
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    assert not response.startswith('Error')

def test_gemini_story_generation():
    gemini = GeminiAPI()
    prompt = "Create a short story about a cat."
    response = gemini.generate_content(prompt)
    print(f"Story Response: {response}")  # For debugging
    assert response is not None
    assert len(response) > 100