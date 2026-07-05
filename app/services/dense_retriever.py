from database.qdrant import qdrant

from app.config.settings import settings

from app.services.embedding_service import (
    get_embedding_service,
)


class DenseRetriever:

    def __init__(self):

        self.embedding = get_embedding_service()

    def retrieve(
        self,
        query: str,
        k: int = 10,
    ):

        vector = self.embedding.embed_query(query)

        results = qdrant.query_points(

            collection_name=settings.QDRANT_COLLECTION,

            query=vector.tolist(),

            limit=k,

        )

        return [
            (
                point.payload["chunk_id"],
                point.score,
            )
            for point in results.points
        ]