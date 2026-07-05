from fastapi import APIRouter

from pydantic import BaseModel

from rag.chat import RAGPipeline


router = APIRouter()

pipeline = RAGPipeline()


class ChatRequest(BaseModel):

    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    answer = pipeline.chat(
        request.question
    )

    return {
        "answer": answer
    }