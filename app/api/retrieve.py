from fastapi import APIRouter

from pydantic import BaseModel

# from app.services.retrieval_service import (
#     RetrievalService,
# )
from app.services.hyde_service import get_hyde_service
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
    import time

    start = time.time()


    
    chunks = service.retrieve(
        request.query
    )

    print(time.time() - start)

    return [

        {
            "id": chunk.id,
            "page": chunk.page,
            "text": chunk.text,
        }

        for chunk in chunks

    ]

@router.post("/retrieve/hyde")
def hyde(query: Query):

    doc = get_hyde_service().generate(query.query)

    return {
        "query": query.query,
        "hypothetical_document": doc,
        }
