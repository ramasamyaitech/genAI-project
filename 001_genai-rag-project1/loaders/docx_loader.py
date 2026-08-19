from pathlib import Path

from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document

from config import logger


class DocxLoader:

    def load(self, file_path: str) -> list[Document]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(file_path)

        logger.info(f"Loading DOCX: {file_path}")

        loader = Docx2txtLoader(str(path))

        documents = loader.load()

        logger.info(f"Loaded {len(documents)} document(s)")

        return documents