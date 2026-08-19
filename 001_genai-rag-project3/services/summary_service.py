from models.llm import LLMModel
from prompts.summary_prompts import SUMMARY_PROMPT


class SummaryService:

    def __init__(self):

        self.llm = LLMModel().get_model()

    def summarize(
        self,
        document: str,
        max_words: int
    ) -> str:

        prompt = SUMMARY_PROMPT.invoke({
            "document": document,
            "max_words": max_words
        })

        response = self.llm.invoke(prompt)

        return response.content