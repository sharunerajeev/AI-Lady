"""
Main configuration module for AI Insurance Assistant.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "AI Insurance Assistant"
    app_version: str = "1.0.0"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # Model Provider Selection: "fallback", "ollama", "azure"
    model_provider: str = "fallback"

    # Ollama Settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "phi3:mini"

    # Azure OpenAI Settings
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = ""
    azure_openai_api_version: str = "2024-02-15-preview"

    # Database
    database_url: str = "sqlite+aiosqlite:///./insurance_assistant.db"

    # AI Settings
    embedding_model: str = "all-MiniLM-L6-v2"
    max_tokens: int = 500
    temperature: float = 0.7

    # Vector Store
    vector_store_path: str = "./data/vector_store"
    collection_name: str = "insurance_faq"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
