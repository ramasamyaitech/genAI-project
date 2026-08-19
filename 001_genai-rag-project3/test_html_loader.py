from langchain_community.document_loaders import UnstructuredHTMLLoader

loader = UnstructuredHTMLLoader(
    "data/index.html"
)

documents = loader.load()

print("Number of documents:", len(documents))

for document in documents:
    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)