from fastapi import APIRouter

from pydantic import BaseModel

# from app.services.retrieval_service import (
#     RetrievalService,
# )

from app.services.hybrid_retrieval_service import (
    HybridRetrievalService
)

router = APIRouter()

service = HybridRetrievalService()


class Query(BaseModel):

    query: str


@router.post("/retrieve")
def retrieve(
    request: Query,
):

    chunks = service.retrieve(
        request.query
    )

    return [

        {
            "id": chunk.id,
            "page": chunk.page,
            "text": chunk.text,
        }

        for chunk in chunks

    ]