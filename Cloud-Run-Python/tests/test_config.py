# tests/test_config.py
import pytest
import os

def test_env_variables(load_env):
    """Test that all required environment variables are present and valid"""
    assert load_env['PROJECT_ID'] == 'nebula-nlp-429123'
    assert load_env['DB_NAME'] == 'wordpress'
    assert load_env['DB_USER'] == 'wordpress_user'
    assert len(load_env['DB_PASSWORD']) > 0
    assert len(load_env['GEMINI_API_KEY']) > 0
    
    # Test database connection variables
    assert load_env['DB_HOST'] in ['10.128.0.11', '35.209.209.243']  # Allow both internal and external IPs
    assert load_env['DB_PORT'] in ['5432', '6432']  # Allow both direct and pgBouncer ports
    
    print("\nEnvironment variables verified:")
    for key, value in load_env.items():
        if key != 'DB_PASSWORD' and key != 'GEMINI_API_KEY':
            print(f"{key}: {value}")
        else:
            print(f"{key}: {'*' * len(value)}")  # Mask sensitive values