from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, ChatOllama


# ============================================================
# 1. Configuration
# ============================================================

VECTORSTORE_PATH = Path("data/vectorstore")

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:1b"


# ============================================================
# 2. Load Embedding Model
# ============================================================

embedding_model = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)


# ============================================================
# 3. Load Existing FAISS Vector Store
# ============================================================

vectorstore = FAISS.load_local(
    str(VECTORSTORE_PATH),
    embedding_model,
    allow_dangerous_deserialization=True
)


# ============================================================
# 4. Load LLM
# ============================================================

llm = ChatOllama(
    model=LLM_MODEL,
    temperature=0
)


# ============================================================
# 5. User Question
# ============================================================

question = "Where was Rahul going one morning?"


# ============================================================
# 6. Retrieve Relevant Documents
# ============================================================

docs = vectorstore.similarity_search(
    question,
    k=2
)


# ============================================================
# 7. Display Retrieved Documents
# ============================================================

print("\n==============================")
print("QUESTION")
print("==============================")

print(question)


print("\n==============================")
print("RETRIEVED DOCUMENTS")
print("==============================")


for i, doc in enumerate(docs, start=1):

    print(f"\n--- Chunk {i} ---")

    print(doc.page_content)

    print("\nMetadata:")
    print(doc.metadata)


# ============================================================
# 8. Build Context
# ============================================================

context = "\n\n".join(
    doc.page_content
    for doc in docs
)


# ============================================================
# 9. Create RAG Prompt
# ============================================================

prompt = f"""
You are a helpful question-answering assistant.

Answer the question using ONLY the information provided
in the context.

If the answer is not available in the context, say:
"I don't know based on the provided document."

Keep the answer short and direct.

Context:
{context}

Question:
{question}

Answer:
"""


# ============================================================
# 10. Generate Final Answer
# ============================================================

response = llm.invoke(prompt)


# ============================================================
# 11. Display Final Answer
# ============================================================

print("\n==============================")
print("FINAL ANSWER")
print("==============================")

print(response.content)

