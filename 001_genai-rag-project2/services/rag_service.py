# from langchain_core.prompts import ChatPromptTemplate

# from models import OllamaModel
# from services.retrieval_service import RetrievalService


# class RAGService:

#     def __init__(self):

#         self.model = OllamaModel()

#         self.llm = self.model.get_llm()

#         self.retriever = RetrievalService()

#         self.prompt = ChatPromptTemplate.from_template(
#             """
# You are a helpful AI assistant.

# Answer the user's question using ONLY the provided context.

# If the answer is not available in the context,
# say:

# "I don't have enough information in the provided documents."

# Do not make up information.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
#         )

#     def ask(self, question: str):

#         documents = self.retriever.retrieve(question)

#         context = "\n\n".join(
#             document.page_content
#             for document in documents
#         )

#         prompt = self.prompt.format(
#             context=context,
#             question=question
#         )

#         response = self.llm.invoke(prompt)

#         sources = [
#             {
#                 "page": doc.metadata.get("page"),
#                 "source": doc.metadata.get("source")
#             }
#             for doc in documents
#         ]

#         return {
#             "answer": response.content,
#             "sources": sources
#         }


# =============================================



# from langchain_core.prompts import ChatPromptTemplate

# from services.retrieval_service import RetrievalService
# from services.llm_service import LLMService


# class RAGService:

#     def __init__(self):

#         self.retriever = RetrievalService()
#         self.llm_service = LLMService()

#         self.prompt = ChatPromptTemplate.from_template(
#             """
# You are a question-answering assistant.

# Answer the question using ONLY the provided context.

# If the answer is present in the context, give a direct and concise answer.

# If the answer is not present in the context, say:
# "I don't have enough information in the provided documents."

# Context:
# {context}

# Question:
# {question}

# Answer:
# """
#         )

#     def ask(self, question: str):

#         results = self.retriever.retrieve(question)

#         if not results:
#             return {
#                 "answer": (
#                     "I don't have enough information "
#                     "in the provided documents."
#                 ),
#                 "sources": []
#             }

#         documents = []
#         sources = []

#         # Handle both:
#         # 1. Document
#         # 2. (Document, score)

#         for item in results:

#             if isinstance(item, tuple) and len(item) == 2:

#                 document, score = item

#             else:

#                 document = item
#                 score = None

#             documents.append(document)

#             sources.append({
#                 "source": document.metadata.get("source"),
#                 "page": document.metadata.get("page"),
#                 "score": float(score) if score is not None else None
#             })

#         # Build context
#         context = "\n\n".join(
#             document.page_content
#             for document in documents
#         )

#         # Create prompt
#         prompt = self.prompt.format(
#             context=context,
#             question=question
#         )

#         # Generate answer
#         answer = self.llm_service.generate(prompt)

#         return {
#             "answer": answer,
#             "sources": sources
#         }



# =============================================


# from pathlib import Path

# from langchain_community.vectorstores import FAISS

# from models import OllamaModel
# from utils.config import settings


# class RAGService:

#     def __init__(self):

#         # Initialize Ollama
#         self.model = OllamaModel()

#         # Embedding model
#         self.embeddings = self.model.get_embeddings()

#         # Load FAISS
#         self.vector_store = None

#         self.load_vector_store()

#     # ---------------------------------------------------------
#     # Load FAISS vector database
#     # ---------------------------------------------------------
#     def load_vector_store(self):

#         vector_path = Path(settings.VECTOR_DB_PATH)

#         if not vector_path.exists():
#             print(
#                 f"Vector store not found: {vector_path}"
#             )
#             return

#         self.vector_store = FAISS.load_local(
#             str(vector_path),
#             self.embeddings,
#             allow_dangerous_deserialization=True
#         )

#         print(
#             f"FAISS vector store loaded from: {vector_path}"
#         )

#     # ---------------------------------------------------------
#     # Retrieve documents
#     # ---------------------------------------------------------
#     def retrieve_documents(self, question: str):

#         if self.vector_store is None:
#             raise ValueError(
#                 "Vector store is not loaded. "
#                 "Please upload/ingest a document first."
#             )

#         results = self.vector_store.similarity_search_with_score(
#             question,
#             k=settings.TOP_K
#         )

#         print("\n" + "=" * 70)
#         print("RETRIEVAL DEBUG")
#         print("=" * 70)

#         documents = []

#         for index, (document, score) in enumerate(
#             results,
#             start=1
#         ):

#             print("\n" + "-" * 70)
#             print(f"RESULT {index}")
#             print("-" * 70)

#             print("SOURCE:")
#             print(
#                 document.metadata.get(
#                     "source_file",
#                     document.metadata.get("source")
#                 )
#             )

#             print("PAGE:")
#             print(
#                 document.metadata.get(
#                     "page",
#                     0
#                 )
#             )

#             print("SCORE:")
#             print(score)

#             print("CONTENT:")
#             print(document.page_content)

#             # Similarity threshold
#             if score <= settings.SIMILARITY_THRESHOLD:

#                 documents.append(
#                     (document, score)
#                 )

#         print("\n" + "=" * 70)

#         return documents

#     # ---------------------------------------------------------
#     # Create context
#     # ---------------------------------------------------------
#     def create_context(self, documents):

#         if not documents:
#             return ""

#         context_parts = []

#         for document, score in documents:

#             content = document.page_content.strip()

#             if content:
#                 context_parts.append(content)

#         return "\n\n".join(context_parts)

#     # ---------------------------------------------------------
#     # Create prompt
#     # ---------------------------------------------------------
#     def create_prompt(
#         self,
#         question: str,
#         context: str
#     ):

#         prompt = f"""
# You are an enterprise document question-answering assistant.

# Your job is to answer the user's question using ONLY
# the information contained in the provided context.

# IMPORTANT RULES:

# 1. Do not use outside knowledge.
# 2. Do not guess.
# 3. Do not invent information.
# 4. If the answer exists in the context, answer directly.
# 5. If the answer does not exist in the context, say:
#    "I don't have enough information in the provided documents."
# 6. Keep the answer concise.
# 7. Pay close attention to names and numbers.

# CONTEXT:
# -------------------------
# {context}
# -------------------------

# QUESTION:
# {question}

# ANSWER:
# """

#         return prompt

#     # ---------------------------------------------------------
#     # Ask LLM
#     # ---------------------------------------------------------
#     def generate_answer(
#         self,
#         question: str,
#         context: str
#     ):

#         prompt = self.create_prompt(
#             question,
#             context
#         )

#         print("\n" + "=" * 70)
#         print("LLM PROMPT")
#         print("=" * 70)

#         print(prompt)

#         print("=" * 70)

#         # IMPORTANT:
#         # Change this method if your OllamaModel uses
#         # another method name.
#         response = self.model.generate(
#             prompt
#         )

#         return response

#     # ---------------------------------------------------------
#     # Complete RAG
#     # ---------------------------------------------------------
#     def ask(self, question: str):

#         question = question.strip()

#         if not question:
#             raise ValueError(
#                 "Question cannot be empty."
#             )

#         # 1. Retrieve
#         documents = self.retrieve_documents(
#             question
#         )

#         # 2. No relevant documents
#         if not documents:

#             return {
#                 "answer": (
#                     "I don't have enough information "
#                     "in the provided documents."
#                 ),
#                 "sources": []
#             }

#         # 3. Create context
#         context = self.create_context(
#             documents
#         )

#         # 4. Generate answer
#         answer = self.generate_answer(
#             question,
#             context
#         )

#         # 5. Build sources
#         sources = []

#         for document, score in documents:

#             source = {
#                 "source": document.metadata.get(
#                     "source_file",
#                     document.metadata.get(
#                         "source",
#                         "unknown"
#                     )
#                 ),
#                 "page": document.metadata.get(
#                     "page",
#                     0
#                 ),
#                 "score": round(
#                     float(score),
#                     4
#                 )
#             }

#             sources.append(source)

#         return {
#             "answer": answer.strip(),
#             "sources": sources
#         }



# ==============================================


from langchain_core.prompts import ChatPromptTemplate

from services.retrieval_service import RetrievalService
from services.llm_service import LLMService


class RAGService:

    def __init__(self):

        self.retriever = RetrievalService()
        self.llm_service = LLMService()

        self.prompt = ChatPromptTemplate.from_template(
            """
You are a question-answering assistant.

Answer the question using ONLY the provided context.

Rules:
1. If the answer is present in the context, answer directly.
2. Do not use outside knowledge.
3. Do not make up or assume information.
4. Keep the answer concise and clear.
5. If the answer is not present in the context, say:
   "I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
        )

    def ask(self, question: str):

        # Retrieve relevant documents
        results = self.retriever.retrieve(question)

        if not results:
            return {
                "answer": (
                    "I don't have enough information "
                    "in the provided documents."
                ),
                "sources": []
            }

        documents = []
        sources = []

        for item in results:

            # similarity_search_with_score()
            # returns (Document, score)
            if isinstance(item, tuple) and len(item) == 2:

                document, score = item

            # similarity_search()
            # returns Document
            else:

                document = item
                score = None

            documents.append(document)

            sources.append({
                "source": document.metadata.get("source"),
                "page": document.metadata.get("page"),
                "score": (
                    float(score)
                    if score is not None
                    else None
                )
            })

        # Combine retrieved chunks
        context = "\n\n".join(
            document.page_content.strip()
            for document in documents
            if document.page_content.strip()
        )

        # Create prompt
        prompt = self.prompt.format(
            context=context,
            question=question
        )

        # Generate answer
        answer = self.llm_service.generate(prompt)

        return {
            "answer": answer.strip(),
            "sources": sources
        }