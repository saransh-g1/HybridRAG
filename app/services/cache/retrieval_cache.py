import hashlib
import json

from functools import lru_cache

from app.services.cache.cache_manager import (
    get_cache_manager,
)


class RetrievalCache:

    PREFIX = "retrieval"

    TTL = 60 * 60

    def __init__(self):

        self.redis = get_cache_manager().redis

        self.hits = 0

        self.misses = 0

    def _key(
        self,
        query: str,
    ):

        return (
            f"{self.PREFIX}:"
            + hashlib.sha256(
                query.encode()
            ).hexdigest()
        )

    def get(
        self,
        query: str,
    ):

        value = self.redis.get(
            self._key(query)
        )

        if value is None:

            self.misses += 1

            return None

        self.hits += 1

        return json.loads(value)

    def set(
        self,
        query: str,
        chunk_ids,
        scores,
    ):

        self.redis.setex(

            self._key(query),

            self.TTL,

            json.dumps(
                {
                    "chunk_ids": chunk_ids,
                    "scores": scores,
                }
            ),
        )

    def stats(self):

        total = self.hits + self.misses

        return {

            "hits": self.hits,

            "misses": self.misses,

            "hit_rate": self.hits / max(total, 1),
        }


@lru_cache
def get_retrieval_cache():

    return RetrievalCache()