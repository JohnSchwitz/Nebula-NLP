# src/utils/db_utils.py
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