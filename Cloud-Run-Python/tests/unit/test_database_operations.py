# tests/unit/test_database_operations.py
import pytest
from src.database.db_operations import DatabaseOperations

@pytest.fixture
def db():
    return DatabaseOperations(use_pgbouncer=False)

def test_save_and_retrieve_story(db):
    # Test data
    user_id = 1
    story_name = "Test Story"
    story_content = "This is a test story content."
    
    try:
        # Save story
        story_id = db.save_story(user_id, story_name, story_content)
        assert story_id is not None
        
        # Retrieve story
        stories = db.get_user_stories(user_id)
        found_story = next((s for s in stories if s[0] == story_id), None)
        
        assert found_story is not None
        assert found_story[1] == story_name
        assert found_story[2] == story_content
    except Exception as e:
        pytest.fail(f"Story save/retrieve test failed: {str(e)}")

def test_get_gemini_settings(db):
    try:
        settings = db.get_gemini_settings()
        assert settings is not None
        assert len(settings) == 6  # id, story_instructions, narrative_instructions, api_key, temperature, max_tokens
        assert isinstance(settings[4], float)  # temperature
        assert isinstance(settings[5], int)    # max_tokens
    except Exception as e:
        pytest.fail(f"Gemini settings test failed: {str(e)}")