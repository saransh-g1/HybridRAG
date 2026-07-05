from fastapi import APIRouter

from pydantic import BaseModel

from rag.chat import RAGPipeline

from app.graph.workflow import get_graph
from app.services.cache.response_cache import (
    get_response_cache,
)

router = APIRouter()

pipeline = RAGPipeline()


class ChatRequest(BaseModel):

    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    # answer = pipeline.chat(
    #     request.question
    # )

    # return {
    #     "answer": answer
    # }

    graph = get_graph()
    cache = get_response_cache()

    cached = cache.get(request.question)

    if cached:
        return cached

    result = graph.invoke(request.question)

    answer = result["answer"]

    cache.set(request.question, result)

    return {
        "answer": result["answer"],
        "supported": result["supported"],
        "retrieval_good": result["retrieval_good"],
        "retrieval_attempts": result["retrieval_attempts"],
        "generation_attempts": result["generation_attempts"],
    }