from functools import lru_cache

import numpy as np

from fastembed import TextEmbedding

from app.config.settings import settings
from app.services.cache.embedding_cache import (
    get_embedding_cache,
)


class EmbeddingService:

    def __init__(self):

        self.model = TextEmbedding(
            model_name=settings.EMBEDDING_MODEL
        )

        self.cache = get_embedding_cache()

    def embed_documents(
        self,
        texts: list[str],
    ):

        vectors = []

        missing = []

        missing_index = []

        for i, text in enumerate(texts):

            cached = self.cache.get(text)

            if cached is not None:

                vectors.append(
                    np.array(cached)
                )

            else:

                vectors.append(None)

                missing.append(text)

                missing_index.append(i)

        if missing:

            generated = list(
                self.model.embed(missing)
            )

            for idx, text, vector in zip(
                missing_index,
                missing,
                generated,
            ):

                self.cache.set(
                    text,
                    vector,
                )

                vectors[idx] = vector

        return vectors

    def embed_query(
        self,
        query: str,
    ):

        cached = self.cache.get(query)

        if cached is not None:

            return np.array(cached)

        embedding = list(
            self.model.embed([query])
        )[0]

        self.cache.set(
            query,
            embedding,
        )

        return embedding


@lru_cache
def get_embedding_service():
    return EmbeddingService()