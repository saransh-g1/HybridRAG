from rank_bm25 import BM25Okapi
import re
from app.db.session import SessionLocal
from app.repositories.chunk_repository import ChunkRepository


class BM25Service:

    def __init__(self):

        self.index = None
        self.chunk_ids = []
        self.corpus = []

        self.rebuild_index()

    def rebuild_index(self):

        print("Building BM25 Index...")

        db = SessionLocal()

        repo = ChunkRepository(db)

        chunks = repo.get_all()

        db.close()

        self.corpus = []
        self.chunk_ids = []

        for chunk in chunks:

            text = chunk.text or ""

            tokens = self.tokenize(text)

            self.corpus.append(tokens)

            self.chunk_ids.append(chunk.id)

        if len(self.corpus):

            self.index = BM25Okapi(self.corpus)

        else:

            self.index = None

        print(f"Indexed {len(self.chunk_ids)} chunks")

    def tokenize(self, text: str):

        return re.findall(r"\w+", text.lower())

    def retrieve(
        self,
        query: str,
        k: int = 20,
    ):

        if self.index is None:

            return []

        scores = self.index.get_scores(
            self.tokenize(query)
        )

        ranked = sorted(

            zip(self.chunk_ids, scores),

            key=lambda x: x[1],

            reverse=True,

        )

        return ranked[:k]