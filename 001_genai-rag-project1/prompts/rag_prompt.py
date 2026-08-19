from langchain_core.prompts import ChatPromptTemplate

from .system_prompt import SYSTEM_PROMPT


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT,
        ),
        (
            "human",
            """
Context:

{context}

Question:

{question}
"""
        )
    ]
)