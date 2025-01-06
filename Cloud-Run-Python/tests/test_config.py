# tests/test_config.py
def test_env_variables(load_env):
    """Test that all required environment variables are loaded"""
    assert all(load_env.values()), "Missing environment variables"