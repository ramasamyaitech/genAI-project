from pydantic import BaseModel, Field


class CustomerExtractionRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class CustomerExtractionResponse(BaseModel):

    name: str | None = None
    email: str | None = None
    phone: str | None = None
    city: str | None = None