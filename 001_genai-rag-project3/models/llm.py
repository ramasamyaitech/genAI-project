from langchain_ollama import ChatOllama

from config import settings


class LLMModel:

    def __init__(self):

        self.llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.LLM_MODEL,
            temperature=0,
            num_predict=settings.MAX_TOKENS
        )

    def get_model(self):
        return self.llm

    def get_structured_model(self, schema):

        return self.llm.with_structured_output(schema)