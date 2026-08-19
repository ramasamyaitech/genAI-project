from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from config import logger, settings
from embeddings import EmbeddingModel


class FAISSStore:
    """
    Wrapper around LangChain FAISS vector store.
    """

    def __init__(self):

        self.embedding = EmbeddingModel().get_model()

        self.index_path = Path(settings.VECTOR_DB_PATH)

        self.vector_store = None

    def create(self, documents: list[Document]):

        logger.info("Creating FAISS index...")

        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding
        )

        self.save()

        logger.info("FAISS index created successfully.")

    def save(self):

        if self.vector_store is None:
            raise ValueError("Vector store not initialized.")

        self.index_path.mkdir(parents=True, exist_ok=True)

        self.vector_store.save_local(
            folder_path=str(self.index_path)
        )

        logger.info(f"Saved index to {self.index_path}")

    def load(self):

        if not self.index_path.exists():
            raise FileNotFoundError(
                f"Index not found: {self.index_path}"
            )

        self.vector_store = FAISS.load_local(
            folder_path=str(self.index_path),
            embeddings=self.embedding,
            allow_dangerous_deserialization=True
        )

        logger.info("FAISS index loaded.")

    # def add_documents(self, documents: list[Document]):

    #     if self.vector_store is None:
    #         self.load()

    #     self.vector_store.add_documents(documents)

    #     self.save()

    #     logger.info(f"Added {len(documents)} documents.")

    
    def add_documents(self, documents: list[Document]):

        if self.vector_store is None:
            self.load()

        batch_size = 100

        total = len(documents)

        for i in range(0, total, batch_size):
            batch = documents[i:i + batch_size]

            logger.info(
                f"Embedding batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size}"
            )

            self.vector_store.add_documents(batch)

        self.save()

        logger.info(f"Added {total} documents.")
    
    def similarity_search(
        self,
        query: str,
        k: int = 4
    ) -> list[Document]:

        if self.vector_store is None:
            self.load()

        logger.info(f"Searching: {query}")

        return self.vector_store.similarity_search(
            query=query,
            k=k
        )