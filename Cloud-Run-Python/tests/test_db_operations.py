# tests/test_db_operations.py
import pytest
import logging

logger = logging.getLogger(__name__)

def test_database_connection(db):
    """Test PostgreSQL connection"""
    logger.info("Testing database connection")
    try:
        conn = db.get_connection()
        assert conn is not None
        cur = conn.cursor()
        
        logger.debug("Executing test query")
        cur.execute("SELECT 1")
        result = cur.fetchone()
        assert result[0] == 1
        
        logger.info("Database connection successful")
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        pytest.fail(f"Database connection failed: {str(e)}")

def test_story_operations(db):
    """Test story save and retrieve operations"""
    logger.info("Testing story operations")
    test_data = {
        "user_id": 1,
        "story_name": "Test Story",
        "story_content": "This is a test story."
    }
    
    story_id = None
    try:
        # Save story
        logger.debug("Saving test story")
        story_id = db.save_story(
            test_data["user_id"],
            test_data["story_name"],
            test_data["story_content"]
        )
        logger.info(f"Story saved with ID: {story_id}")
        assert story_id is not None
        
        # Retrieve stories
        logger.debug("Retrieving user stories")
        stories = db.get_user_stories(test_data["user_id"])
        assert len(stories) > 0
        logger.info(f"Retrieved {len(stories)} stories")
        
        # Find our test story
        found_story = next((s for s in stories if s[0] == story_id), None)
        assert found_story is not None
        assert found_story[1] == test_data["story_name"]
        assert found_story[2] == test_data["story_content"]
        logger.info("Story verification successful")
        
    except Exception as e:
        logger.error(f"Story operations failed: {str(e)}")
        pytest.fail(f"Story operations failed: {str(e)}")
    finally:
        # Cleanup
        if story_id:
            try:
                logger.debug(f"Cleaning up test story {story_id}")
                db.delete_story(story_id)
                logger.info("Test story cleaned up")
            except Exception as e:
                logger.error(f"Cleanup failed: {str(e)}")