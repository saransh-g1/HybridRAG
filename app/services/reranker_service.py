from functools import lru_cache
from dataclasses import dataclass
from sentence_transformers import CrossEncoder
from app.services.cache.retrieval_cache import (
    get_retrieval_cache,
)

@dataclass
class RetrievedChunk:
    chunk: object
    score: float


class RerankerService:

    def __init__(self):

        print("Loading CrossEncoder...")

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

        self.cache = get_retrieval_cache()

    def rerank(
        self,
        query: str,
        chunks,
        top_k: int = 5,
    ):

        if not chunks:
            return []

        pairs = [
            (query, chunk.text)
            for chunk in chunks
        ]

        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True,
        )


        self.cache.set(

            query,

            chunk_ids,

            scores,
        )

        return [
            RetrievedChunk(
                chunk=chunk,
                score=score,
            )
            for chunk, score in ranked[:top_k]
        ]


@lru_cache
def get_reranker():

    return RerankerService()