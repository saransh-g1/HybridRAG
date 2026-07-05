from collections import defaultdict

def reciprocal_rank_fusion(*rankings, k=60):
    scores = defaultdict(float)

    for ranking in rankings:
        for rank, doc in enumerate(ranking):
            scores[str(doc)] += 1 / (k + rank)

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )