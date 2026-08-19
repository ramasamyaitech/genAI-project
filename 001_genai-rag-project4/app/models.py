from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=3,
        description="User question"
    )


class QuestionResponse(BaseModel):

    answer: str

    sources: list[str] = []


class UploadResponse(BaseModel):

    filename: str

    message: str

    chunks_created: int