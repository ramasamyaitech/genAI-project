from pathlib import Path

from services.ingestion_service import IngestionService


pdf_path = Path("data/documents/boy_story.pdf")

if not pdf_path.exists():
    raise FileNotFoundError(
        f"PDF not found: {pdf_path.resolve()}"
    )

print(f"PDF found: {pdf_path.resolve()}")

service = IngestionService()

service.ingest(str(pdf_path))