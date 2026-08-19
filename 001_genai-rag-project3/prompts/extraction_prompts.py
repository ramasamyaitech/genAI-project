from langchain_core.prompts import ChatPromptTemplate


EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an information extraction system.

Extract customer information from the input text.

Return these fields:

- name
- email
- phone
- city

Rules:

1. Extract information exactly from the input.
2. Do not invent information.
3. If a field is not available, return null.
4. Rahul is the customer's name if the text says
   "Rahul lives in Chennai".
5. Return structured data only.
"""
    ),

    (
        "human",
        """
Customer Text:

{text}
"""
    )
])