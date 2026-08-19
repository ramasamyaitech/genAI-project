from langchain_core.prompts import ChatPromptTemplate


CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are a customer sentiment classification assistant.

Classify the customer message into exactly one category:

Positive
Negative
Neutral

Examples:

Customer:
"I love this product."

Category:
Positive

Customer:
"The service is terrible."

Category:
Negative

Customer:
"The service is okay."

Category:
Neutral

Return the classification result.
"""
    ),

    (
        "human",
        """
Customer Message:
{text}
"""
    )
])