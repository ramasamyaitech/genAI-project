from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


# 1. Prompt
prompt = ChatPromptTemplate.from_template(
    """
    Explain {topic} in simple English.
    Give one example.
    """
)


# 2. Model
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)


# 3. Output Parser
parser = StrOutputParser()


# 4. Create Chain
chain = prompt | llm | parser


# 5. Run Chain
result = chain.invoke({
    "topic": "Vector Database"
})


print(result)



# =========================



# Why use Chains?

# Without a chain:

# prompt_result = prompt.invoke(data)


# llm_result = llm.invoke(prompt_result)


# final_result = parser.invoke(llm_result)

# With a chain:

# chain = prompt | llm | parser


# result = chain.invoke(data)

# So the code becomes shorter, cleaner, and easier to maintain.

# Chain in RAG

# A RAG application can also use a chain:

# User Question
#       ↓
# Retriever
#       ↓
# Relevant Documents
#       ↓
# Prompt
#       ↓
# LLM
#       ↓
# Output Parser
#       ↓
# Answer

# For example:

# rag_chain = retriever | prompt | llm | parser

# Simple interview answer:

# A LangChain chain connects multiple components such as Prompt, LLM, Retriever, and Output Parser so that data flows automatically from one step to another