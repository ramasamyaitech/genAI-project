from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


# 1. Prompt
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple English with one example."
)


# 2. LLM
llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0
)


# 3. Output Parser
parser = StrOutputParser()


# 4. Chain
chain = prompt | llm | parser


# 5. Execute
result = chain.invoke({
    "topic": "Vector Database"
})


print(result)

# ===========================================================

# What LangChain is doing
#                 LangChain
#                     │
#         ┌───────────┼───────────┐
#         ↓           ↓           ↓
#       Prompt       LLM       Parser
#         │           │           │
#         └───────────┼───────────┘
#                     ↓
#                Final Answer
# LangChain is useful for
# Prompt templates
# Chains / Runnable pipelines
# Output parsers
# RAG applications
# Document loading
# Text splitting
# Embeddings
# Vector databases
# Retrievers
# Agents
# Conversation/memory workflows
# RAG example

# For your RAG learning, LangChain can connect:

# PDF
#  ↓
# Document Loader
#  ↓
# Text Splitter
#  ↓
# Chunks
#  ↓
# Embedding Model
#  ↓
# Vector Database
#  ↓
# Retriever
#  ↓
# Prompt
#  ↓
# LLM
#  ↓
# Answer

# So, in simple words:

# LangChain is a framework that provides reusable components for connecting an LLM with prompts, documents, vector databases, tools, retrievers, and application logic.