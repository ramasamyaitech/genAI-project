from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama import ChatOllama


class Person(BaseModel):
    name: str
    age: int
    city: str


parser = PydanticOutputParser(
    pydantic_object=Person
)


prompt = ChatPromptTemplate.from_template("""
Extract information from this text.

Text:
{text}

Return ONLY valid JSON.

Example:
{{
    "name": "Ramasamy",
    "age": 39,
    "city": "Chennai"
}}
""")


llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)


# Prompt → LLM → Parser
chain = prompt | llm | parser


result = chain.invoke({
    "text": "Ramasamy is 39 years old and lives in Chennai."
})


print(result)

print("Name:", result.name)
print("Age:", result.age)
print("City:", result.city)