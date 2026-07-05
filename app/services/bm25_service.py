from rank_bm25 import BM25Okapi

from app.db.session import SessionLocal
from app.repositories.chunk_repository import ChunkRepository


class BM25Service:

    def __init__(self):
        self.index = None
        self.chunk_ids = []
        self._build()

    def _build(self):
        db = SessionLocal()

        repo = ChunkRepository(db)

        chunks = repo.get_all()

        corpus = []

        self.chunk_ids = []

        for chunk in chunks:
            corpus.append(chunk.text.lower().split())
            self.chunk_ids.append(chunk.id)

        self.index = BM25Okapi(corpus)

        db.close()

    def retrieve(
        self,
        query: str,
        k: int = 20,
    ):

        scores = self.index.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            zip(self.chunk_ids, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:k]