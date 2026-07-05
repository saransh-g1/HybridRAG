from app.db.session import SessionLocal
from app.repositories.chunk_repository import ChunkRepository

from app.services.bm25_service import BM25Service
from app.services.dense_retriever import DenseRetriever
from app.services.rrf_service import RRFService
from app.config.settings import settings
from app.services.hyde_service import get_hyde_service
from app.services.crag_service import get_crag_service
from app.services.reranker_service import (
    get_reranker,
)

class HybridRetrievalService:

    def __init__(self):
        self.reranker = get_reranker()
        self.dense = DenseRetriever()
        self.bm25 = BM25Service()
        self.rrf = RRFService()
        self.hyde = get_hyde_service()
        self.crag = get_crag_service()

    def retrieve(
        self,
        query: str,
        k: int = 10,
    ):

        retrieval_query = query

        if settings.USE_HYDE:
            retrieval_query = self.hyde.generate(query)

        dense_results = self.dense.retrieve(
            retrieval_query,
            20,
        )

        sparse_results = self.bm25.retrieve(
            retrieval_query,
            20,
        )

        fused = self.rrf.fuse(
            dense_results,
            sparse_results,
        )

        ids = [
            doc_id
            for doc_id, _ in fused[:k]
        ]

        db = SessionLocal()

        repo = ChunkRepository(db)

        chunks = repo.get_by_ids(ids)

        db.close()

        reranked = self.reranker.rerank(query, chunks)
        print("sfesoiifwe")
        print(type(reranked))

        for i, item in enumerate(reranked):
            print(f"Index {i}: {type(item)}")
            print(item)

        scores = [float(item.score) for item in reranked]

        good = self.crag.is_context_good(scores)

        if not good:
            return {
                "status": "LOW_CONFIDENCE",
                "chunks": reranked,
            }

        return {
            "status": "SUCCESS",
            "chunks": reranked,
        }