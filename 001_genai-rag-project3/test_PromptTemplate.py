from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

# prompt = ChatPromptTemplate.from_template(
#     "Explain {topic} in simple English with an example."
# )

prompt = ChatPromptTemplate.from_template(
    """
    Explain {topic} for a {level} learner.
    Give one simple example.
    """
)

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)

parser = StrOutputParser()

chain = prompt | llm | parser

# result = chain.invoke({
#     "topic": "Embeddings"
# })

result = chain.invoke({
    "topic": "Vector Database",
    "level": "beginner"
})

print(result)