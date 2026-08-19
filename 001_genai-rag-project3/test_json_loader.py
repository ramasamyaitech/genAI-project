from langchain_community.document_loaders import JSONLoader


loader = JSONLoader(
    file_path="data/data.json",
    jq_schema=".",
    text_content=False
)

documents = loader.load()

print("Number of documents:", len(documents))

for document in documents:
    print("\nContent:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)
    
    
# pip install jq