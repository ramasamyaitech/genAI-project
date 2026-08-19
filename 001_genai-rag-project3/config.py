from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "GenAI Prompt Engineering API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "llama3.2:1b"

    TEMPERATURE: float = 0.0
    MAX_TOKENS: int = 2048

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()