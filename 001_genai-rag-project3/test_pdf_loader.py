from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    "data/aws.pdf"
)

documents = loader.load()

print("Number of pages:", len(documents))

for document in documents:
    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)