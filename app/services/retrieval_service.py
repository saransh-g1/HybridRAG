from app.db.session import SessionLocal

from app.repositories.chunk_repository import (
    ChunkRepository,
)

from app.services.dense_retriever import (
    DenseRetriever,
)

from app.services.cache.retrieval_cache import (
    get_retrieval_cache,
)


class RetrievalService:

    def __init__(self):

        self.retriever = DenseRetriever()
        self.cache = get_retrieval_cache()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):

        cached = self.cache.get(query)

        if cached:
            db = SessionLocal()
            repo = ChunkRepository(db)
            chunks = repo.get_by_ids(
                cached["chunk_ids"]
            )
            db.close()
            return {

                "status": "SUCCESS",

                "chunks": chunks,

                "scores": cached["scores"],
            }

        points = self.retriever.retrieve(
            query,
            k,
        )

        ids = [
            chunk_id
            for chunk_id, _ in points
        ]

        db = SessionLocal()

        repo = ChunkRepository(db)

        chunks = repo.get_by_ids(ids)

        db.close()

        return chunks