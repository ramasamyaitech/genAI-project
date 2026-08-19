from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    LLM_MODEL: str = "llama3.2:3b"
    EMBEDDING_MODEL: str = "nomic-embed-text"

    DOCUMENT_PATH: str = "data/documents"
    VECTOR_DB_PATH: str = "data/vectorstore"

    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.4

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

# Create directories automatically
Path(settings.DOCUMENT_PATH).mkdir(
    parents=True,
    exist_ok=True
)

Path(settings.VECTOR_DB_PATH).mkdir(
    parents=True,
    exist_ok=True
)