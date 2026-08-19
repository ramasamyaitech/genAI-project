from langchain_core.prompts import ChatPromptTemplate


SUMMARY_PROMPT = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an expert document summarization assistant.

Summarize the provided document accurately.

Rules:

1. Do not invent information.
2. Preserve important facts.
3. Use simple English.
4. Remove unnecessary details.
5. Follow the requested word limit.
"""
    ),

    (
        "human",
        """
Maximum words:
{max_words}

Document:
{document}

Summary:
"""
    )
])