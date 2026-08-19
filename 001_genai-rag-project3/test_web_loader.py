from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    "https://example.com"
)

documents = loader.load()

print("Number of documents:", len(documents))

for document in documents:
    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)