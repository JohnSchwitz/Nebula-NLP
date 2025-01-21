import pytest
from utils.db_utils import DatabaseOperations
import os
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def db():
    """Database fixture that ensures table exists"""
    config = {
        'host': '35.209.209.243',
        'port': '5432',
        'database': 'wordpress',
        'user': 'wordpress_user',
        'password': 'ZaQ!2wsx'
    }
    db_ops = DatabaseOperations(config)
    # Ensure table exists before running tests
    db_ops.create_stories_table()
    return db_ops

def test_database_connection(db):
    """Test PostgreSQL connection"""
    try:
        conn = db.get_connection()
        assert conn is not None
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        assert result[0] == 1
        print("Database connection successful")
        cur.close()
        conn.close()
    except Exception as e:
        pytest.fail(f"Database connection failed: {str(e)}")

def test_story_operations(db):
    """Test story save and retrieve operations"""
    test_data = {
        "user_id": 1,
        "story_name": "Test Story",
        "story_content": "This is a test story."
    }
    
    story_id = None
    try:
        # Save story
        story_id = db.save_story(
            test_data["user_id"],
            test_data["story_name"],
            test_data["story_content"]
        )
        assert story_id is not None
        print(f"Story saved with ID: {story_id}")
        
        # Retrieve stories
        stories = db.get_user_stories(test_data["user_id"])
        assert len(stories) > 0
        print(f"Retrieved {len(stories)} stories")
        
        # Find our test story
        found_story = next((s for s in stories if s[0] == story_id), None)
        assert found_story is not None
        assert found_story[1] == test_data["story_name"]
        assert found_story[2] == test_data["story_content"]
        print("Story verification successful")
        
    except Exception as e:
        pytest.fail(f"Story operations failed: {str(e)}")
    finally:
        # Cleanup: Delete test story
        if story_id:
            try:
                db.delete_story(story_id)
                print("Test story cleaned up")
            except Exception as e:
                print(f"Cleanup failed: {str(e)}")

def test_table_exists(db):
    """Test that the stories table exists"""
    try:
        with db.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'wp_user_stories'
                    );
                """)
                exists = cur.fetchone()[0]
                assert exists, "Stories table does not exist"
                print("Stories table exists")
    except Exception as e:
        pytest.fail(f"Table check failed: {str(e)}")