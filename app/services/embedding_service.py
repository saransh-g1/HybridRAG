from functools import lru_cache

from fastembed import TextEmbedding

from app.config.settings import settings


class EmbeddingService:
    def __init__(self):
        self.model = TextEmbedding(
            model_name=settings.EMBEDDING_MODEL
        )

    def embed_documents(self, texts: list[str]):
        """
        Generate embeddings for multiple documents.
        Returns a list of numpy arrays.
        """
        return list(self.model.embed(texts))

    def embed_query(self, query: str):
        """
        Generate embedding for a single query.
        """
        return list(self.model.embed([query]))[0]


@lru_cache
def get_embedding_service():
    return EmbeddingService()