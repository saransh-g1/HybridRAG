from collections import defaultdict


class RRFService:

    def fuse(
        self,
        dense,
        sparse,
        k=60,
    ):

        scores = defaultdict(float)

        for rank, (doc, _) in enumerate(dense):
            scores[doc] += 1 / (k + rank)

        for rank, (doc, _) in enumerate(sparse):
            scores[doc] += 1 / (k + rank)

        return sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )