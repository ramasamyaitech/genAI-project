from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import settings
from app.models import (
    QuestionRequest,
    QuestionResponse,
    UploadResponse
)
from app.rag import rag_service


app = FastAPI(
    title="Investment Banking RAG API",
    description="Modular RAG application for investment banking documents",
    version="1.0.0"
)


@app.get("/health")
def health_check():

    return {
        "status": "UP",
        "service": "Investment Banking RAG"
    }


@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = (
        Path(settings.DOCUMENT_PATH)
        / file.filename
    )

    try:

        contents = await file.read()

        with open(file_path, "wb") as f:

            f.write(contents)

        chunks_created = rag_service.add_document(
            str(file_path)
        )

        return UploadResponse(
            filename=file.filename,
            message="PDF uploaded and indexed successfully.",
            chunks_created=chunks_created
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(request: QuestionRequest):

    try:

        result = rag_service.ask_question(
            request.question
        )

        return QuestionResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )