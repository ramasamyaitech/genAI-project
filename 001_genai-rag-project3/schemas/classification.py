from typing import Literal

from pydantic import BaseModel, Field


class ClassificationRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )


class ClassificationResponse(BaseModel):

    category: Literal[
        "Positive",
        "Negative",
        "Neutral"
    ]

    confidence: float = Field(
        ge=0,
        le=1
    )

    reason: str