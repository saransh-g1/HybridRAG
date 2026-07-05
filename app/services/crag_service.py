from functools import lru_cache


class CRAGService:

    def __init__(self, threshold: float = 0.35):
        self.threshold = threshold

    def is_context_good(self, reranked_scores):

        if not reranked_scores:
            return False

        best_score = reranked_scores[0]

        return best_score >= self.threshold


@lru_cache
def get_crag_service():
    return CRAGService()