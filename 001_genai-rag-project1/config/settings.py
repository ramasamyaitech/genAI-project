from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    APP_NAME: str

    HOST: str

    PORT: int

    OLLAMA_BASE_URL: str

    OLLAMA_MODEL: str

    EMBEDDING_MODEL: str

    VECTOR_DB: str

    VECTOR_DB_PATH: str

    POSTGRES_HOST: str

    POSTGRES_PORT: int

    POSTGRES_DB: str

    POSTGRES_USER: str

    POSTGRES_PASSWORD: str

    REDIS_HOST: str

    REDIS_PORT: int

    UPLOAD_DIR: str
    
    TOP_K: int
    
    OLLAMA_TEMPERATURE: float

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()