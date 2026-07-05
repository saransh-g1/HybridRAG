from fastapi import APIRouter

from app.services.ingestion_service import IngestionService

router = APIRouter()

service = IngestionService()


@router.post("/ingest")
def ingest():

    count = service.ingest()

    return {
        "indexed_chunks": count
    }