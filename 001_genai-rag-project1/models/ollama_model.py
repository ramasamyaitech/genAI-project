from langchain_ollama import ChatOllama

from config import logger, settings


class OllamaModel:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            logger.info(
                f"Loading model: {settings.OLLAMA_MODEL}"
            )

            cls._instance.model = ChatOllama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=settings.OLLAMA_TEMPERATURE,
            )

        return cls._instance

    def get_model(self):

        return self.model