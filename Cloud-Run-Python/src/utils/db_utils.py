import psycopg2
import os
from dotenv import load_dotenv

class DatabaseOperations:
    def __init__(self, config=None):
        if config is None:
            load_dotenv()
            self.config = {
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT'),
                'database': os.getenv('DB_NAME'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD')
            }
        else:
            self.config = config

    def get_connection(self):
        return psycopg2.connect(**self.config)

    def save_story(self, user_id, story_name, story_content):
        """Save a story to the database"""
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
                conn.commit()
                return story_id

    def get_user_stories(self, user_id):
        """Get all stories for a user"""
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

    def get_story(self, story_id):
        """Get a specific story by ID"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT user_id, story_name, story
                    FROM wp_user_stories
                    WHERE story_id = %s;
                    """,
                    (story_id,)
                )
                return cur.fetchone()

    def delete_story(self, story_id):
        """Delete a story (useful for test cleanup)"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM wp_user_stories
                    WHERE story_id = %s;
                    """,
                    (story_id,)
                )
                conn.commit()
    def create_stories_table(self):
        """Create the wp_user_stories table if it doesn't exist"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS wp_user_stories (
                        story_id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        story_name TEXT NOT NULL,
                        story TEXT NOT NULL
                    );
                """)
                conn.commit()
                print("Table created or already exists")