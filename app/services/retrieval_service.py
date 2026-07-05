from app.db.session import SessionLocal

from app.repositories.chunk_repository import (
    ChunkRepository,
)

from app.services.dense_retriever import (
    DenseRetriever,
)


class RetrievalService:

    def __init__(self):

        self.retriever = DenseRetriever()

    def retrieve(
        self,
        query: str,
        k: int = 5,
    ):

        points = self.retriever.retrieve(
            query,
            k,
        )

        ids = [
            point.payload["chunk_id"]
            for point in points
        ]

        db = SessionLocal()

        repo = ChunkRepository(db)

        chunks = repo.get_by_ids(ids)

        db.close()

        return chunks