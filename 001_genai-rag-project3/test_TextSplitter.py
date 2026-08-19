from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
AWS S3 is an object storage service.
It is used to store files, images, videos and documents.

Amazon EC2 provides virtual servers in the cloud.
AWS Lambda runs code without managing servers.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}")
    print(chunk)