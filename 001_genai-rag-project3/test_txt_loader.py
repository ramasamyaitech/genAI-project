from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    "data/aws.txt",
    encoding="utf-8"
)

documents = loader.load()

print("Number of documents:", len(documents))

for document in documents:
    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)