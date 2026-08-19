from langchain_ollama import OllamaLLM

from app.config import settings


def get_llm():

    return OllamaLLM(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=settings.LLM_TEMPERATURE
    )