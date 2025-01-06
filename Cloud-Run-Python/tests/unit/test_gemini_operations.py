# tests/unit/test_gemini_operations.py
import pytest
from src.ai.gemini_operations import GeminiOperations
from src.database.db_operations import DatabaseOperations

@pytest.fixture
def gemini():
    db = DatabaseOperations(use_pgbouncer=False)
    return GeminiOperations(db)

def test_generate_story_segment(gemini):
    test_input = "A story about a brave knight and a dragon"
    response = gemini.generate_story_segment(test_input)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    assert not response.startswith('Error')

def test_complete_story(gemini):
    test_story = "Once upon a time, there was a brave knight..."
    response = gemini.complete_story(test_story)
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    assert not response.startswith('Error')