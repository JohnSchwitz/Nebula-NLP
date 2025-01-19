# tests/unit/test_db_utils.py
import pytest
from src.utils.db_utils import DatabaseOperations

def test_database_connection(db):
    """Test database connectivity"""
    try:
        stories = db.get_user_stories(1)
        assert isinstance(stories, list)
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

def test_save_and_retrieve_story(db):
    """Test saving and retrieving a story"""
    test_user_id = 1
    test_story_name = "Test Story"
    test_content = "This is a test story content."
    
    try:
        story_id = db.save_story(test_user_id, test_story_name, test_content)
        assert story_id is not None
        
        stories = db.get_user_stories(test_user_id)
        found_story = next((s for s in stories if s[0] == story_id), None)
        assert found_story is not None
        assert found_story[1] == test_story_name
        assert found_story[2] == test_content
    except Exception as e:
        pytest.fail(f"Story save/retrieve test failed: {str(e)}")