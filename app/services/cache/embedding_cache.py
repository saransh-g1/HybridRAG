import hashlib
import json
from functools import lru_cache

from app.services.cache.cache_manager import (
    get_cache_manager,
)


class EmbeddingCache:

    PREFIX = "embedding"

    TTL = 60 * 60 * 24

    def __init__(self):

        self.redis = get_cache_manager().redis

    def _key(self, text: str):

        return (
            f"{self.PREFIX}:"
            + hashlib.sha256(
                text.encode("utf-8")
            ).hexdigest()
        )

    def get(self, text: str):

        value = self.redis.get(
            self._key(text)
        )

        if value is None:
            return None

        return json.loads(value)

    def set(self, text: str, embedding):

        self.redis.setex(
            self._key(text),
            self.TTL,
            json.dumps(
                embedding.tolist()
            ),
        )


@lru_cache
def get_embedding_cache():
    return EmbeddingCache()