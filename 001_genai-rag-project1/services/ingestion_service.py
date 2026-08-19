from pathlib import Path

from config import logger, settings
from chunking import TextChunker
from loaders import (
    PDFLoader,
    DocxLoader,
    CSVDocumentLoader,
)
from vectorstore import FAISSStore


class IngestionService:

    def __init__(self):

        self.chunker = TextChunker()

        self.vector_store = FAISSStore()

    def ingest(self, file_path: str):

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        logger.info(f"Ingesting {path.name}")

        documents = self._load_document(path)

        chunks = self.chunker.split_documents(documents)

        if self.vector_store.index_path.exists():

            self.vector_store.add_documents(chunks)

        else:

            self.vector_store.create(chunks)

        logger.info("Ingestion completed.")

    def _load_document(self, path: Path):

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return PDFLoader().load(str(path))

        elif suffix == ".docx":
            return DocxLoader().load(str(path))

        elif suffix == ".csv":
            return CSVDocumentLoader().load(str(path))

        else:
            raise ValueError(
                f"Unsupported file type: {suffix}"
            )