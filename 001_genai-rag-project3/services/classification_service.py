from models.llm import LLMModel
from prompts.classification_prompts import CLASSIFICATION_PROMPT


class ClassificationService:

    def __init__(self):

        self.llm = LLMModel().get_model()

    def classify(self, text: str) -> str:

        prompt = CLASSIFICATION_PROMPT.invoke({
            "text": text
        })

        response = self.llm.invoke(prompt)

        return response.content