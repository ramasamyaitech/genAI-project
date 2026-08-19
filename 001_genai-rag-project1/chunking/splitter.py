from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import logger


class TextChunker:
    """
    Splits LangChain Document objects into smaller chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

    def split_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:

        logger.info(
            f"Splitting {len(documents)} document(s)..."
        )

        chunks = self.splitter.split_documents(documents)

        logger.info(
            f"Created {len(chunks)} chunks."
        )

        return chunks