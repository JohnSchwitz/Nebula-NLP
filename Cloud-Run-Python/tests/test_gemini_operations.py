# tests/test_gemini_operations.py
import pytest
import logging
from src.ai.gemini_direct import GeminiAPI
from src.ai.story_generator import StoryGenerator

logger = logging.getLogger(__name__)

@pytest.fixture
def gemini():
    return GeminiAPI()

@pytest.fixture
def story_generator():
    return StoryGenerator()

def test_gemini_connection(gemini):
    """Test basic Gemini API connectivity"""
    logger.info("Testing Gemini API connection")
    test_prompt = "Write a single sentence test."
    logger.debug(f"Sending prompt: {test_prompt}")
    
    response = gemini.generate_content(test_prompt)
    logger.info(f"Received response: {response}")
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    assert not response.startswith('Error')

def test_story_generation(story_generator):
    """Test story generation functionality"""
    logger.info("Testing story generation")
    prompt = "Create a short story about a scientist."
    logger.debug(f"Sending story prompt: {prompt}")
    
    response = story_generator.create_story(prompt)
    
    # Add error checking
    if response is None:
        logger.error("Story generation returned None")
        pytest.fail("Story generation failed")
    
    if isinstance(response, str) and response.startswith('Error'):
        logger.error(f"Story generation error: {response}")
        pytest.fail(f"Story generation failed: {response}")
    
    logger.info(f"Generated story excerpt: {response[:200]}...")
    
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0