from langchain_ollama import OllamaEmbeddings

from config import logger, settings


class EmbeddingModel:
    """
    Singleton wrapper around the Ollama embedding model.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            logger.info(
                f"Loading embedding model: {settings.EMBEDDING_MODEL}"
            )

            cls._instance.model = OllamaEmbeddings(
                model=settings.EMBEDDING_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
            )

        return cls._instance

    def get_model(self):
        return self.model