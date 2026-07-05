from rag.retrieval.retriever import Retriever
from rag.retrieval.context import build_context

from rag.prompts.rag_prompt import SYSTEM_PROMPT

from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService

class RAGPipeline:

    def __init__(self):

        self.retriever = RetrievalService()

        self.llm = LLMService()

    def chat(
        self,
        question: str,
    ):

        chunks = self.retriever.retrieve(question)

        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question,
        )

        return self.llm.generate(prompt)