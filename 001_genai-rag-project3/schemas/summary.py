from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):

    document: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )

    max_words: int = Field(
        default=200,
        ge=50,
        le=1000
    )


class SummaryResponse(BaseModel):

    summary: str