from rank_bm25 import BM25Okapi

class SparseRetriever:

    def __init__(self):
        self.documents = []
        self.bm25 = None

    def build(self, docs):
        self.documents = docs
        tokenized = [d.split() for d in docs]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query, k=20):
        scores = self.bm25.get_scores(query.split())

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:k]