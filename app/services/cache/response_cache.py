import hashlib
import json
from functools import lru_cache

from app.services.cache.cache_manager import (
    get_cache_manager,
)


class ResponseCache:

    PREFIX = "response"

    TTL = 60 * 60

    def __init__(self):

        self.redis = get_cache_manager().redis

        self.hits = 0
        self.misses = 0

    def _key(self, question: str):

        return (
            f"{self.PREFIX}:"
            + hashlib.sha256(
                question.strip().lower().encode()
            ).hexdigest()
        )

    def get(self, question: str):

        value = self.redis.get(
            self._key(question)
        )

        if value is None:

            self.misses += 1
            return None

        self.hits += 1

        return json.loads(value)

    def set(
        self,
        question: str,
        response,
    ):

        self.redis.setex(

            self._key(question),

            self.TTL,

            json.dumps(response),
        )

    def clear(self):

        cursor = 0

        while True:

            cursor, keys = self.redis.scan(
                cursor,
                match=f"{self.PREFIX}:*",
                count=500,
            )

            if keys:
                self.redis.delete(*keys)

            if cursor == 0:
                break

    def stats(self):

        total = self.hits + self.misses

        return {

            "hits": self.hits,

            "misses": self.misses,

            "hit_rate": self.hits / max(total, 1),
        }


@lru_cache
def get_response_cache():

    return ResponseCache()