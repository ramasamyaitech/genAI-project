from pydantic import BaseModel


class QuestionResponse(BaseModel):

    answer: str


class UploadResponse(BaseModel):

    message: str