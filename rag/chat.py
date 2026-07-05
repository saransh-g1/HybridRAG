from rag.prompts.rag_prompt import SYSTEM_PROMPT

from app.services.llm_service import LLMService
from app.services.hybrid_retrieval_service import HybridRetrievalService

class RAGPipeline:

    def __init__(self):

        self.retriever = HybridRetrievalService()

        self.llm = LLMService()

    def chat(
        self,
        question: str,
    ):

        retrieval = self.retriever.retrieve(question)

        if retrieval["status"] == "LOW_CONFIDENCE":

            return (
                "I couldn't find sufficiently relevant information "
                "in the indexed documents to answer confidently."
            )

        chunks = retrieval["chunks"]

        context = "\n\n".join(
            chunk.chunk.text
            for chunk in chunks
        )

        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question,
        )
        answer = self.llm.generate(prompt)

        result = self.self_rag.evaluate(
            question,
            context,
            answer,
        )

        if result["supported"]:
            return answer

        return (
            "I couldn't verify this answer from the retrieved documents.\n\n"
            f"Reason: {result['reason']}"
        )