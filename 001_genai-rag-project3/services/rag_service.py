from models.llm import LLMModel
from prompts.rag_prompts import RAG_PROMPT


class RAGService:

    def __init__(self):

        self.llm = LLMModel().get_model()

    def ask(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = RAG_PROMPT.invoke({
            "context": context,
            "question": question
        })

        response = self.llm.invoke(prompt)

        return response.content