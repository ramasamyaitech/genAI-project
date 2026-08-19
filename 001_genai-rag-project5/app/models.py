from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Question to ask about the uploaded documents"
    )


class QuestionResponse(BaseModel):

    answer: str

    sources: list[str] = Field(
        default_factory=list
    )


class UploadResponse(BaseModel):

    filename: str

    message: str

    chunks_created: int

    document_hash: str


class DocumentInfo(BaseModel):

    filename: str

    document_hash: str

    chunks: int

    size_bytes: int


class HealthResponse(BaseModel):

    status: str

    service: str

    vectorstore_loaded: bool