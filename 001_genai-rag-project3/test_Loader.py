from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


# ============================================================
# STEP 1: DOCUMENT LOADER
# ============================================================

loader = TextLoader(
    "data/aws.txt",
    encoding="utf-8"
)

documents = loader.load()

print("=" * 60)
print("STEP 1: DOCUMENT LOADER")
print("=" * 60)

print("Number of documents:", len(documents))

for document in documents:
    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)


# ============================================================
# STEP 2: TEXT SPLITTER
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

chunks = text_splitter.split_documents(documents)

print("\n")
print("=" * 60)
print("STEP 2: TEXT SPLITTER")
print("=" * 60)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk.page_content)
    print("Metadata:", chunk.metadata)


# ============================================================
# STEP 3: EMBEDDING MODEL
# ============================================================

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

print("\n")
print("=" * 60)
print("STEP 3: EMBEDDING MODEL")
print("=" * 60)

print("Embedding model:", "nomic-embed-text")


# ============================================================
# STEP 4: CREATE VECTOR DATABASE
# ============================================================

vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

print("\n")
print("=" * 60)
print("STEP 4: FAISS VECTOR DATABASE")
print("=" * 60)

print("Chunks successfully converted into embeddings.")
print("Embeddings successfully stored in FAISS.")


# ============================================================
# STEP 5: USER QUESTION
# ============================================================

question = "Which AWS service is used to store files?"


print("\n")
print("=" * 60)
print("STEP 5: USER QUESTION")
print("=" * 60)

print("Question:", question)


# ============================================================
# STEP 6: SIMILARITY SEARCH
# ============================================================

results = vectorstore.similarity_search(
    question,
    k=2
)


print("\n")
print("=" * 60)
print("STEP 6: SIMILARITY SEARCH RESULTS")
print("=" * 60)

for i, result in enumerate(results):

    print(f"\nResult {i + 1}")

    print("Content:")
    print(result.page_content)

    print("\nMetadata:")
    print(result.metadata)


# ============================================================
# STEP 7: SIMILARITY SEARCH WITH SCORE
# ============================================================

results_with_scores = vectorstore.similarity_search_with_score(
    question,
    k=2
)


print("\n")
print("=" * 60)
print("STEP 7: RESULTS WITH SCORES")
print("=" * 60)

for document, score in results_with_scores:

    print("\nContent:")
    print(document.page_content)

    print("Score:")
    print(score)