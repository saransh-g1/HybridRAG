from qdrant_client import QdrantClient

from app.config.settings import settings

qdrant = QdrantClient(
    url=settings.QDRANT_URL,
    check_compatibility=False,
)