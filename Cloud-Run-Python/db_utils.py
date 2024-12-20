# db_utils.py
import psycopg2
from psycopg2.pool import SimpleConnectionPool
import os


# Database Configuration from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 5432))  # Default port 5432 if not set
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
MIN_CONNECTIONS = 10
MAX_CONNECTIONS = 20
pool = None

def create_connection_pool():
   global pool
   try:
        # Test direct connection
        conn_test = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn_test.close()
        print("Direct connection successful")

        pool = SimpleConnectionPool(
           minconn=MIN_CONNECTIONS,
           maxconn=MAX_CONNECTIONS,
           host=DB_HOST,
           port=DB_PORT,
           database=DB_NAME,
           user=DB_USER,
           password=DB_PASSWORD
       )
        print("Connection pool created successfully.")
        return pool
   except psycopg2.Error as e:
        print(f"Error creating connection pool: {e}")
        return None

def save_story(user_id, story_name, story_content):
    """Saves a story to the database."""
    # ... (Implementation remains the same) ...

def delete_story(story_id):
    """Deletes a story from the database."""
    try:
        conn = pool.getconn()
        cur = conn.cursor()
        cur.execute("DELETE FROM wp_user_stories WHERE story_id = %s", (story_id,))
        conn.commit()
        cur.close()
        pool.putconn(conn)
        return True
    except psycopg2.Error as e:
        print(f"Error deleting story: {e}")
        if conn:
            conn.rollback()
            pool.putconn(conn)
        return False
    
def get_all_stories(pool, user_id):
    """Retrieves all stories for a specific user."""
    try:
        conn = pool.getconn()
        cur = conn.cursor()
        cur.execute("SELECT story_id, story_name, story FROM wp_user_stories WHERE user_id = %s", (user_id,))
        stories = cur.fetchall()
        cur.close()
        pool.putconn(conn)
        return stories
    except psycopg2.Error as e:
        print(f"Error getting stories: {e}")
        if conn:
            pool.putconn(conn)
        return None

def close_connection_pool():
    global pool
    if pool:
        pool.closeall()