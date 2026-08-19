from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_ollama import ChatOllama

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template(
    """
    Extract the person's information.

    Text:
    {text}

    Return JSON with:
    - name
    - age
    - city

    {format_instructions}
    """
)

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)

chain = prompt | llm | parser

result = chain.invoke({
    "text": "Ramasamy is 39 years old and lives in Chennai.",
    "format_instructions": parser.get_format_instructions()
})

print(result)
print(type(result))