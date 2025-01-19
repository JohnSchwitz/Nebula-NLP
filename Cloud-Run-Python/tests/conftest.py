# tests/conftest.py
import pytest
import logging
import os
import sys
from dotenv import load_dotenv
from utils.db_utils import DatabaseOperations

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

@pytest.fixture(scope="session")
def load_env():
    """Load environment variables"""
    load_dotenv()
    required_vars = [
        'PROJECT_ID',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'GEMINI_API_KEY'
    ]
    
    # Check if all required variables are present
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        pytest.fail(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {var: os.getenv(var) for var in required_vars}

@pytest.fixture(scope="session")
def db(load_env):
    """Database fixture that ensures table exists"""
    config = {
        'host': '35.209.209.243',
        'port': '5432',
        'database': load_env['DB_NAME'],
        'user': load_env['DB_USER'],
        'password': load_env['DB_PASSWORD']
    }
    db_ops = DatabaseOperations(config)
    db_ops.create_stories_table()
    return db_ops