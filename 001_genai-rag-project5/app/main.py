from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import settings
from app.document_manager import document_manager
from app.models import (
    DocumentInfo,
    HealthResponse,
    QuestionRequest,
    QuestionResponse,
    UploadResponse
)
from app.rag import rag_service


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Production-style Investment Banking "
        "Retrieval Augmented Generation API"
    ),
    version=settings.APP_VERSION
)


# ==================================================
# Health
# ==================================================

@app.get(
    "/health",
    response_model=HealthResponse
)
def health_check():

    return HealthResponse(
        status="UP",
        service=settings.APP_NAME,
        vectorstore_loaded=(
            rag_service.vectorstore is not None
        )
    )


# ==================================================
# Upload
# ==================================================

@app.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(
    file: UploadFile = File(...)
):

    # --------------------------------------------------
    # Filename validation
    # --------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    safe_filename = Path(
        file.filename
    ).name

    if not safe_filename.lower().endswith(
        settings.ALLOWED_EXTENSION
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # --------------------------------------------------
    # Read file
    # --------------------------------------------------

    contents = await file.read()

    max_size = (
        settings.MAX_FILE_SIZE_MB
        * 1024
        * 1024
    )

    if len(contents) > max_size:

        raise HTTPException(
            status_code=413,
            detail=(
                f"File size exceeds "
                f"{settings.MAX_FILE_SIZE_MB} MB limit."
            )
        )

    if len(contents) == 0:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # --------------------------------------------------
    # Save PDF
    # --------------------------------------------------

    document_directory = Path(
        settings.DOCUMENT_PATH
    )

    document_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = (
        document_directory
        / safe_filename
    )

    try:

        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(
                contents
            )

        # --------------------------------------------------
        # Index
        # --------------------------------------------------

        result = rag_service.add_document(
            str(file_path)
        )

        return UploadResponse(
            filename=safe_filename,
            message=(
                "PDF uploaded and indexed successfully."
            ),
            chunks_created=result["chunks"],
            document_hash=result["document_hash"]
        )

    except ValueError as exc:

        # Remove file if indexing failed
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )

    except Exception as exc:

        print(
            f"Document processing error: {exc}"
        )

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to process and index the PDF."
            )
        )


# ==================================================
# Ask
# ==================================================

@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):

    try:

        result = rag_service.ask_question(
            request.question
        )

        return QuestionResponse(
            answer=result["answer"],
            sources=result["sources"]
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        print(
            f"Question processing error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to process the question."
            )
        )


# ==================================================
# Documents
# ==================================================

@app.get(
    "/documents",
    response_model=list[DocumentInfo]
)
def list_documents():

    documents = (
        document_manager.list_documents()
    )

    return documents