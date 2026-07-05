from typing import List, TypedDict

from app.db.models import Chunk


class GraphState(TypedDict):

    question: str

    retrieval_query: str

    chunks: List[Chunk]

    scores: List[float]

    context: str

    answer: str

    retrieval_good: bool

    supported: bool

    retrieval_attempts: int

    generation_attempts: int

    route: str