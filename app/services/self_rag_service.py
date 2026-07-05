from functools import lru_cache

from app.services.llm_service import LLMService
import json


class SelfRAGService:

    def __init__(self):

        self.llm = LLMService()

    def evaluate(
        self,
        question,
        context,
        answer,
    ):

        prompt = f"""
        You are evaluating whether an AI answer is supported by the retrieved context.

        Question:
        {question}

        Retrieved Context:
        {context}

        Generated Answer:
        {answer}

        Evaluate whether the answer is completely supported by the retrieved context.

        Return ONLY valid JSON.

        Example:

        {{
            "supported": true,
            "reason": "The answer is completely supported by the retrieved context."
        }}

        or

        {{
            "supported": false,
            "reason": "The retrieved context does not contain enough evidence."
        }}

        Do not include markdown.
        Do not include explanations.
        Return JSON only.
        """

        response = self.llm.generate(prompt)
        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        if response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        result = json.loads(response)

        return result


@lru_cache
def get_self_rag():

    return SelfRAGService()