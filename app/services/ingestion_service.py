from pathlib import Path
import hashlib
from uuid import uuid4

from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
)

from app.db.session import SessionLocal
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository

from app.config.settings import settings

from database.qdrant import qdrant

from app.services.loader_service import LoaderService
from app.services.splitter_service import SplitterService

from app.services.embedding_service import get_embedding_service
from app.services.bm25_service import BM25Service
from app.services.cache.cache_manager import (
    get_cache_manager,
)

class IngestionService:

    def __init__(self):

        self.embedding = get_embedding_service()
        self.loader = LoaderService()
        self.splitter = SplitterService()
        self.cache_manager = get_cache_manager()

    def _hash_file(self, path: str):

        h = hashlib.sha256()

        with open(path, "rb") as f:
            h.update(f.read())

        return h.hexdigest()

    def ingest(self):

        db = SessionLocal()

        document_repo = DocumentRepository(db)

        chunk_repo = ChunkRepository(db)

        files = self.loader.load_directory()

        for file_path, documents in files.items():

            print(f"Processing {file_path}")

            chunks = self.splitter.split(documents)

        collections = [
            c.name
            for c in qdrant.get_collections().collections
        ]

        if settings.QDRANT_COLLECTION not in collections:

            qdrant.create_collection(

                collection_name=settings.QDRANT_COLLECTION,

                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

        grouped = {}

        for chunk in chunks:

            source = chunk.metadata["source"]

            grouped.setdefault(source, [])

            grouped[source].append(chunk)

        total = 0

        for source, chunk_list in grouped.items():

            file_hash = self._hash_file(source)

            if document_repo.get_by_hash(file_hash):

                print(source, "already indexed")

                continue

            document = document_repo.create(

                filename=Path(source).name,

                file_hash=file_hash,

            )

            texts = []

            saved = []

            for idx, chunk in enumerate(chunk_list):

                c = chunk_repo.create(

                    document_id=document.id,

                    chunk_index=idx,

                    page=chunk.metadata.get("page", 0),

                    text=chunk.page_content,

                )

                saved.append(c)

                texts.append(chunk.page_content)

            vectors = self.embedding.embed_documents(texts)

            points = []

            for chunk, vector in zip(saved, vectors):

                points.append(

                    PointStruct(

                        id=str(uuid4()),

                        vector=vector.tolist(),

                        payload={

                            "chunk_id": chunk.id,

                            "document_id": document.id,

                        },

                    )

                )

            qdrant.upsert(

                collection_name=settings.QDRANT_COLLECTION,

                points=points,

            )

            total += len(points)

        db.commit()
        BM25Service().rebuild_index()
        db.close()
        get_cache_manager().invalidate_rag()
        return total