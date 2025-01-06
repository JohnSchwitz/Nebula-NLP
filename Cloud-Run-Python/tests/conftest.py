# tests/conftest.py
import pytest
from src.utils.db_utils import DatabaseOperations
from src.utils.pdf_utils import StoryPDF

@pytest.fixture
def db():
    return DatabaseOperations(use_pgbouncer=False)

@pytest.fixture
def pdf():
    return StoryPDF()