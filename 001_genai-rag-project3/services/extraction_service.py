import re

from models.llm import LLMModel

from prompts.extraction_prompts import (
    EXTRACTION_PROMPT
)

from schemas.extraction import (
    CustomerExtractionResponse
)


class ExtractionService:

    def __init__(self):

        model = LLMModel()

        self.llm = model.get_structured_model(
            CustomerExtractionResponse
        )

    def extract(
        self,
        text: str
    ) -> CustomerExtractionResponse:

        # -------------------------------------------------
        # STEP 1: Call LLM
        # -------------------------------------------------

        prompt = EXTRACTION_PROMPT.invoke({
            "text": text
        })

        result = self.llm.invoke(prompt)

        # -------------------------------------------------
        # STEP 2: Deterministic Email Extraction
        # -------------------------------------------------

        if not result.email:

            email_match = re.search(
                r'\b[A-Za-z0-9._%+-]+'
                r'@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
                text
            )

            if email_match:

                result.email = email_match.group(0)

        # -------------------------------------------------
        # STEP 3: Deterministic Phone Extraction
        # -------------------------------------------------

        if not result.phone:

            phone_match = re.search(
                r'\b\d{10}\b',
                text
            )

            if phone_match:

                result.phone = phone_match.group(0)

        # -------------------------------------------------
        # STEP 4: Name Extraction
        # -------------------------------------------------

        if not result.name:

            name_patterns = [

                r'\bMy name is\s+([A-Z][a-zA-Z]+)',

                r'\bname is\s+([A-Z][a-zA-Z]+)',

                r'\b([A-Z][a-zA-Z]+)\s+lives\s+in\b',

                r'\b([A-Z][a-zA-Z]+)\s+is living\s+in\b',

            ]

            for pattern in name_patterns:

                name_match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                )

                if name_match:

                    result.name = (
                        name_match.group(1)
                    )

                    break

        # -------------------------------------------------
        # STEP 5: City Extraction
        # -------------------------------------------------

        if not result.city:

            city_patterns = [

                r'\bliving\s+in\s+([A-Z][a-zA-Z]+)',

                r'\blive\s+in\s+([A-Z][a-zA-Z]+)',

                r'\blives\s+in\s+([A-Z][a-zA-Z]+)',

                r'\bresiding\s+in\s+([A-Z][a-zA-Z]+)',

                r'\bfrom\s+([A-Z][a-zA-Z]+)',

            ]

            for pattern in city_patterns:

                city_match = re.search(
                    pattern,
                    text,
                    re.IGNORECASE
                )

                if city_match:

                    result.city = (
                        city_match.group(1)
                    )

                    break

        # -------------------------------------------------
        # STEP 6: Return structured result
        # -------------------------------------------------

        return result