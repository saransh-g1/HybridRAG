from functools import lru_cache

from app.services.llm_service import LLMService


class HyDEService:

    def __init__(self):
        self.llm = LLMService()

    def generate(self, query: str) -> str:

        prompt = f"""
You are generating a hypothetical document for semantic retrieval.

Write a concise factual paragraph that would likely answer the user's question.

Do not mention that this is hypothetical.
Do not say "I don't know".
Only generate the answer.

Question:
{query}
"""

        return self.llm.generate(prompt).strip()


@lru_cache
def get_hyde_service():
    return HyDEService()