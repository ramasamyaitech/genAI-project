from fastapi import APIRouter

from schemas.common import (
    QuestionRequest,
    AnswerResponse
)

from schemas.summary import (
    SummaryRequest,
    SummaryResponse
)

from schemas.classification import (
    ClassificationRequest,
    ClassificationResponse
)

from schemas.extraction import (
    CustomerExtractionRequest,
    CustomerExtractionResponse
)

from services.rag_service import RAGService
from services.summary_service import SummaryService
from services.classification_service import (
    ClassificationService
)
from services.extraction_service import (
    ExtractionService
)


router = APIRouter(prefix="/api/v1")


rag_service = RAGService()
summary_service = SummaryService()
classification_service = ClassificationService()
extraction_service = ExtractionService()


@router.post(
    "/rag",
    response_model=AnswerResponse
)
def rag(request: QuestionRequest):

    context = """
    Amazon S3 is an object storage service provided by AWS.
    It is used to store objects such as documents,
    images, videos and backups.
    """

    answer = rag_service.ask(
        question=request.question,
        context=context
    )

    return AnswerResponse(
        answer=answer
    )


@router.post(
    "/summary",
    response_model=SummaryResponse
)
def summarize(request: SummaryRequest):

    result = summary_service.summarize(
        document=request.document,
        max_words=request.max_words
    )

    return SummaryResponse(
        summary=result
    )


@router.post(
    "/classification"
)
def classify(request: ClassificationRequest):

    result = classification_service.classify(
        request.text
    )

    return {
        "result": result
    }


@router.post("/extraction")
def extract(request: CustomerExtractionRequest):

    result = extraction_service.extract(request.text)

    return result