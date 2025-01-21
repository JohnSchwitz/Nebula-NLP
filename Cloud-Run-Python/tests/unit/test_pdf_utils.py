# tests/unit/test_pdf_utils.py
import pytest
from utils.pdf_utils import generate_story_pdf
from io import BytesIO

def test_generate_story_pdf():
    """Test PDF generation"""
    story_name = "Test Story"
    story_content = "This is a test story content."

    pdf_buffer = generate_story_pdf(story_name, story_content)
    assert isinstance(pdf_buffer, bytes)  # Assert that it's bytes
    assert pdf_buffer                 # Check if it's not empty
