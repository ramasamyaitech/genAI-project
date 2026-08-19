from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# STEP 1: Create Documents
# ============================================================

documents = [
    Document(
        page_content="Chennai is the capital city of Tamil Nadu. "
                     "It is located on the eastern coast of India."
    ),
    Document(
        page_content="Mumbai is the capital city of Maharashtra. "
                     "It is a major financial center in India."
    ),
    Document(
        page_content="Bengaluru is the capital city of Karnataka. "
                     "It is known as a major technology hub."
    ),
    Document(
        page_content="Amazon S3 is an AWS object storage service. "
                     "It is used to store files, images, videos and documents."
    ),
]


print("=" * 60)
print("STEP 1: DOCUMENTS")
print("=" * 60)

for document in documents:
    print(document.page_content)
    print()


# ============================================================
# STEP 2: Split Documents into Chunks
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = text_splitter.split_documents(documents)


print("=" * 60)
print("STEP 2: CHUNKS")
print("=" * 60)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk.page_content)


# ============================================================
# STEP 3: Create Embedding Model
# ============================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


print("\n")
print("=" * 60)
print("STEP 3: EMBEDDING MODEL")
print("=" * 60)

print("Embedding model created.")


# ============================================================
# STEP 4: Convert Chunks into Embeddings
# ============================================================

chunk_texts = [
    chunk.page_content
    for chunk in chunks
]

vectors = embeddings.embed_documents(chunk_texts)


print("=" * 60)
print("STEP 4: EMBEDDINGS")
print("=" * 60)

print("Number of vectors:", len(vectors))

for i, vector in enumerate(vectors[:2]):
    print(f"\nVector {i + 1}:")
    print(vector[:10])
    print("Vector dimension:", len(vector))


# ============================================================
# STEP 5: Store Embeddings in FAISS
# ============================================================

vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)


print("\n")
print("=" * 60)
print("STEP 5: FAISS VECTOR DATABASE")
print("=" * 60)

print("Documents successfully stored in FAISS.")


# ============================================================
# STEP 6: User Question
# ============================================================

question = "Which city is the capital of Tamil Nadu?"


print("\n")
print("=" * 60)
print("STEP 6: USER QUESTION")
print("=" * 60)

print(question)


# ============================================================
# STEP 7: Convert Question into Embedding
# ============================================================

query_vector = embeddings.embed_query(question)


print("\n")
print("=" * 60)
print("STEP 7: QUERY EMBEDDING")
print("=" * 60)

print("First 10 numbers:")
print(query_vector[:10])

print("Vector dimension:")
print(len(query_vector))


# ============================================================
# STEP 8: Similarity Search
# ============================================================

results = vectorstore.similarity_search(
    question,
    k=2
)


print("\n")
print("=" * 60)
print("STEP 8: SIMILARITY SEARCH")
print("=" * 60)

for i, result in enumerate(results):
    print(f"\nResult {i + 1}:")
    print(result.page_content)


# ============================================================
# STEP 9: Similarity Search with Scores
# ============================================================

results_with_scores = vectorstore.similarity_search_with_score(
    question,
    k=2
)


print("\n")
print("=" * 60)
print("STEP 9: SIMILARITY SEARCH WITH SCORE")
print("=" * 60)

for document, score in results_with_scores:
    print("\nDocument:")
    print(document.page_content)

    print("Score:")
    print(score)