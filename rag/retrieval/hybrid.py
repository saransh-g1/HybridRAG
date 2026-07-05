from rag.retrieval.dense import DenseRetriever
from rag.retrieval.sparse import SparseRetriever
from rag.retrieval.fusion import reciprocal_rank_fusion


class HybridRetriever:

    def __init__(self):
        self.dense = DenseRetriever()
        self.sparse = SparseRetriever()

    def retrieve(self, query):
        dense = self.dense.retrieve(query)
        sparse = self.sparse.retrieve(query)

        return reciprocal_rank_fusion(
            dense,
            sparse,
        )