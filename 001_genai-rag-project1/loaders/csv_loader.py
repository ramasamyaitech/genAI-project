from pathlib import Path

from langchain_community.document_loaders import CSVLoader
from langchain_core.documents import Document

from config import logger


class CSVDocumentLoader:

    def load(self, file_path: str) -> list[Document]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        logger.info(f"Loading CSV: {file_path}")

        loader = CSVLoader(file_path=str(path))

        documents = loader.load()

        logger.info(f"Loaded {len(documents)} rows")

        return documents