from langchain_core.documents import Document

from config import logger
from models import OllamaModel
from prompts import RAG_PROMPT
from vectorstore import FAISSStore


class RAGService:

    def __init__(self):

        self.vector_store = FAISSStore()

        self.llm = OllamaModel().get_model()

    def ask(
        self,
        question: str,
        k: int = 4
    ) -> str:

        logger.info(f"Question: {question}")

        documents = self.vector_store.similarity_search(
            query=question,
            k=k
        )

        context = self._build_context(documents)

        prompt = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": question
            }
        )

        response = self.llm.invoke(prompt)

        logger.info("Answer generated.")

        return response.content

    @staticmethod
    def _build_context(
        documents: list[Document]
    ) -> str:

        return "\n\n".join(
            document.page_content
            for document in documents
        )