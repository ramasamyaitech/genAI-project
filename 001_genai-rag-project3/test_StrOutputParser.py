from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in one sentence."
)

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)

parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({
    "topic": "AWS S3"
})

print(result)
print(type(result))