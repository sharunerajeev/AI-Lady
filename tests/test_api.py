"""
Basic tests for AI Insurance Assistant.
Run with: pytest tests/
"""

import pytest
from httpx import AsyncClient
from app.config import get_settings


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health endpoint."""
    # This is a placeholder for actual tests
    # You would import your FastAPI app and test it
    settings = get_settings()
    assert settings.app_name == "AI Insurance Assistant"


def test_settings_load():
    """Test settings configuration."""
    settings = get_settings()
    assert settings.app_version == "1.0.0"
    assert settings.chat_model == "gpt-3.5-turbo"


# Add more tests as needed
