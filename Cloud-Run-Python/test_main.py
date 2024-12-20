# test_main.py
import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


try:
    conn_test = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
   )
    conn_test.close()
    print("Direct connection successful")
except psycopg2.Error as e:
   print(f"Error creating connection: {e}")