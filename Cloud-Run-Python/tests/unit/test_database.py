# tests/unit/test_database.py
import pytest
from src.database.db_operations import StoryDatabase

@pytest.fixture
def db():
    return StoryDatabase(use_pgbouncer=False)  # Use direct connection for testing

def test_database_connection(db):
    """Test basic database connectivity"""
    try:
        stories = db.get_stories_by_user(1)
        assert isinstance(stories, list)
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

def test_save_and_retrieve_story(db):
    """Test saving and retrieving a story"""
    test_user_id = 1
    test_story_name = "Test Story"
    test_content = "This is a test story content."
    
    try:
        # Save story
        story_id = db.save_story(test_user_id, test_story_name, test_content)
        assert story_id is not None
        
        # Retrieve story
        story = db.get_story(story_id)
        assert story is not None
        assert story[0] == test_user_id
        assert story[1] == test_story_name
        assert story[2] == test_content
    except Exception as e:
        pytest.fail(f"Story save/retrieve test failed: {str(e)}")

def test_get_user_stories(db):
    """Test retrieving all stories for a user"""
    test_user_id = 1
    
    try:
        stories = db.get_stories_by_user(test_user_id)
        assert isinstance(stories, list)
        for story in stories:
            assert len(story) == 3  # story_id, story_name, story_content
    except Exception as e:
        pytest.fail(f"Get user stories test failed: {str(e)}")