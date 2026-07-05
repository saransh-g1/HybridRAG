from app.services.cache.embedding_cache import (
    get_embedding_cache,
)

from app.services.cache.retrieval_cache import (
    get_retrieval_cache,
)

from app.services.cache.response_cache import (
    get_response_cache,
)


def cache_metrics():

    return {

        "embedding": get_embedding_cache().stats(),

        "retrieval": get_retrieval_cache().stats(),

        "response": get_response_cache().stats(),
    }