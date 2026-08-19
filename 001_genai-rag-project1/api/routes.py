from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    File,
    UploadFile,
    HTTPException,
)

from config import settings, logger
from services import (
    RAGService,
    IngestionService,
)
from .request_model import QuestionRequest
from .response_model import (
    QuestionResponse,
    UploadResponse,
)

router = APIRouter()

rag_service = RAGService()

ingestion_service = IngestionService()


@router.get("/health")
def health():

    return {
        "status": "UP"
    }


@router.post(
    "/ask",
    response_model=QuestionResponse
)
def ask(request: QuestionRequest):

    try:

        answer = rag_service.ask(
            request.question
        )

        return QuestionResponse(
            answer=answer
        )

    except Exception as error:

        logger.exception(error)

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload(
    file: UploadFile = File(...)
):

    upload_dir = Path(settings.UPLOAD_DIR)

    upload_dir.mkdir(
        exist_ok=True
    )

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    ingestion_service.ingest(
        str(file_path)
    )

    return UploadResponse(
        message="Upload successful"
    )