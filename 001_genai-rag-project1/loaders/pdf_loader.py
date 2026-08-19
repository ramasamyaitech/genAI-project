from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from config import logger


class PDFLoader:

    def load(self, file_path: str) -> list[Document]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        logger.info(f"Loading PDF: {file_path}")

        loader = PyPDFLoader(str(path))

        documents = loader.load()

        logger.info(f"Loaded {len(documents)} pages")

        return documents