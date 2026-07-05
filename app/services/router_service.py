from functools import lru_cache

from app.services.llm_service import LLMService


class RouterService:

    def __init__(self):
        self.llm = LLMService()

    def route(self, question: str) -> str:

        prompt = f"""
Classify the user's question.

Return ONLY one word.

RAG
SQL

Question:

{question}
"""

        result = self.llm.generate(prompt)

        result = result.strip().upper()

        if result not in {"RAG", "SQL"}:
            return "RAG"

        return result


@lru_cache
def get_router():
    return RouterService()