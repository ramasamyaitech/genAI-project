from langchain_ollama import OllamaLLM

from app.config import settings


def get_llm():

    llm = OllamaLLM(
        model=settings.LLM_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.0
    )

    return llm