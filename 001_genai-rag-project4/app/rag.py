from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM

from app.config import settings
from app.document_processor import process_pdf
from app.embeddings import get_embedding_model
from app.ollama_service import get_llm
from app.prompts import RAG_PROMPT


class RAGService:

    def __init__(self):

        self.embedding_model = get_embedding_model()

        self.llm = get_llm()
        
        self.vectorstore = None

        self.load_vectorstore()

    # --------------------------------------------------
    # Load existing FAISS index
    # --------------------------------------------------

    def load_vectorstore(self):

        index_path = Path(
            settings.VECTOR_DB_PATH
        )

        index_file = index_path / "index.faiss"

        if index_file.exists():

            print("Loading existing FAISS vectorstore...")

            self.vectorstore = FAISS.load_local(
                str(index_path),
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

            print("FAISS vectorstore loaded.")

        else:

            print(
                "FAISS vectorstore does not exist yet."
            )

    # --------------------------------------------------
    # Add PDF to vector database
    # --------------------------------------------------

    def add_document(self, file_path: str):

        chunks = process_pdf(file_path)

        if not chunks:

            raise ValueError(
                "No text could be extracted from PDF."
            )

        if self.vectorstore is None:

            print("Creating new FAISS vectorstore...")

            self.vectorstore = FAISS.from_documents(
                chunks,
                self.embedding_model
            )

        else:

            print("Adding documents to existing FAISS...")

            self.vectorstore.add_documents(
                chunks
            )

        self.vectorstore.save_local(
            settings.VECTOR_DB_PATH
        )

        return len(chunks)

    # --------------------------------------------------
    # Retrieve relevant documents
    # --------------------------------------------------

    def retrieve_documents(self, question: str):

        if self.vectorstore is None:

            raise ValueError(
                "Vector database is empty. "
                "Please upload a PDF first."
            )

        documents = self.vectorstore.similarity_search(
            question,
            k=settings.TOP_K
        )

        return documents

    # --------------------------------------------------
    # Generate answer
    # --------------------------------------------------

    def ask_question(self, question: str):

        documents = self.retrieve_documents(
            question
        )

        if not documents:

            return {
                "answer": (
                    "The information is not available "
                    "in the provided documents."
                ),
                "sources": []
            }

        context_parts = []

        sources = set()

        for document in documents:

            content = document.page_content

            source = document.metadata.get(
                "source",
                "Unknown"
            )

            page = document.metadata.get(
                "page"
            )

            if page is not None:

                source_name = (
                    f"{source} - Page {page + 1}"
                )

            else:

                source_name = source

            sources.add(source_name)

            context_parts.append(
                f"Source: {source_name}\n"
                f"{content}"
            )

        context = "\n\n---\n\n".join(
            context_parts
        )

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        answer = self.llm.invoke(prompt)

        return {
            "answer": answer,
            "sources": sorted(sources)
        }


rag_service = RAGService()


def retrieve_documents(question: str):

    return rag_service.retrieve_documents(
        question
    )


def ask_question(question: str):

    return rag_service.ask_question(
        question
    )