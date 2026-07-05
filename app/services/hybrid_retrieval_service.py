from app.db.session import SessionLocal

from app.repositories.chunk_repository import ChunkRepository

from app.services.bm25_service import BM25Service
from app.services.dense_retriever import DenseRetriever
from app.services.rrf_service import RRFService


class HybridRetrievalService:

    def __init__(self):

        self.dense = DenseRetriever()
        self.sparse = BM25Service()
        self.rrf = RRFService()

    def retrieve(self, query):

        dense = self.dense.retrieve(query, 20)

        sparse = self.sparse.retrieve(query, 20)

        fused = self.rrf.fuse(
            dense,
            sparse,
        )

        ids = [

            doc

            for doc, _ in fused[:10]

        ]

        db = SessionLocal()

        repo = ChunkRepository(db)

        chunks = repo.get_by_ids(ids)

        db.close()

        return chunks