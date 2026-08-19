from langchain_community.document_loaders import Docx2txtLoader

loader = Docx2txtLoader(
    "data/sample.docx"
)

documents = loader.load()

print("Number of documents:", len(documents))

for document in documents:
    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)
    
# pip install docx2txt