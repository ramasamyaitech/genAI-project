from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # --------------------------------------------------
    # Application
    # --------------------------------------------------

    APP_NAME: str = "Investment Banking RAG API"
    APP_VERSION: str = "2.0.0"

    # --------------------------------------------------
    # Ollama
    # --------------------------------------------------

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    LLM_MODEL: str = "llama3.2:1b"

    EMBEDDING_MODEL: str = "nomic-embed-text"

    LLM_TEMPERATURE: float = 0.0

    # --------------------------------------------------
    # RAG
    # --------------------------------------------------

    CHUNK_SIZE: int = 800

    CHUNK_OVERLAP: int = 150

    TOP_K: int = 4

    # FAISS L2 distance:
    # Lower score = more similar.
    SIMILARITY_THRESHOLD: float = 1.5

    # --------------------------------------------------
    # Upload
    # --------------------------------------------------

    MAX_FILE_SIZE_MB: int = 50

    ALLOWED_EXTENSION: str = ".pdf"

    # --------------------------------------------------
    # Paths
    # --------------------------------------------------

    DOCUMENT_PATH: str = "data/documents"

    VECTOR_DB_PATH: str = "data/vectorstore"

    METADATA_PATH: str = "data/metadata"

    DOCUMENT_MANIFEST: str = "data/metadata/documents.json"

    # --------------------------------------------------
    # Pydantic
    # --------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # --------------------------------------------------
    # Directory initialization
    # --------------------------------------------------

    def create_directories(self):

        Path(self.DOCUMENT_PATH).mkdir(
            parents=True,
            exist_ok=True
        )

        Path(self.VECTOR_DB_PATH).mkdir(
            parents=True,
            exist_ok=True
        )

        Path(self.METADATA_PATH).mkdir(
            parents=True,
            exist_ok=True
        )


settings = Settings()

settings.create_directories()