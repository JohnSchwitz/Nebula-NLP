# src/database/db_operations.py
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

class DatabaseOperations:
    def __init__(self, use_pgbouncer=False):
        load_dotenv()
        
        self.config = {
            'host': os.getenv('DB_HOST') if not use_pgbouncer else '35.209.209.243',
            'port': '5432' if not use_pgbouncer else '6432',
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }

    def get_connection(self):
        return psycopg2.connect(**self.config)

    # Story Operations
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
                return cur.fetchone()[0]

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

    # Gemini Settings Operations
    def get_gemini_settings(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM wp_gemini ORDER BY id DESC LIMIT 1;")
                return cur.fetchone()

    def update_gemini_settings(self, story_instructions, narrative_instructions, 
                             api_key, temperature, max_tokens):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO wp_gemini 
                    (story_instructions, narrative_instructions, api_key, temperature, max_tokens)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (story_instructions, narrative_instructions, api_key, temperature, max_tokens)
                )
                return cur.fetchone()[0]