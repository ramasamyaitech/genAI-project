from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )


class AnswerResponse(BaseModel):

    answer: str