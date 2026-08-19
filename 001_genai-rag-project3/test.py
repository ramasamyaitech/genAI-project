from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

prompt = ChatPromptTemplate.from_template(
    """Explain this topic in simple English: {question}
    my name is Ramasamy from India, I am a software engineer and I have 10 years of experience in software development. I have worked on various technologies and frameworks. I am passionate about learning new technologies and improving my skills. I am also interested in AI and machine learning. I want to learn more about AWS S3 and how it works. Please explain it to me in simple English."""
)

llm = ChatOllama(model="llama3.2:1b")

parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({
    "question": "what is your name?"
})

print(result)