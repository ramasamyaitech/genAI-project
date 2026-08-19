from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_ollama import ChatOllama


parser = CommaSeparatedListOutputParser()

prompt = ChatPromptTemplate.from_template(
    """
    Give me 5 popular AWS services.

    {format_instructions}
    """
)

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)

chain = prompt | llm | parser

result = chain.invoke({
    "format_instructions": parser.get_format_instructions()
})

print(result)
print(type(result))