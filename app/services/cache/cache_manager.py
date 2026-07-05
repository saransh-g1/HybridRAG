from functools import lru_cache

from database.redis import redis_client


class CacheManager:

    def __init__(self):

        self.redis = redis_client

    def clear_prefix(
        self,
        prefix: str,
    ):

        cursor = 0

        while True:

            cursor, keys = self.redis.scan(
                cursor,
                match=f"{prefix}:*",
                count=500,
            )

            if keys:

                self.redis.delete(*keys)

            if cursor == 0:
                break

    def invalidate_rag(self):

        self.clear_prefix("embedding")
        self.clear_prefix("retrieval")
        self.clear_prefix("response")


@lru_cache
def get_cache_manager():

    return CacheManager()