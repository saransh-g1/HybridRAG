from fastapi import FastAPI

from database.qdrant import qdrant
from app.api.ingest import router as ingest_router
from app.api.chat import router as chat_router
from contextlib import asynccontextmanager

from app.db.base import Base
from app.db.session import engine
from app.api.retrieve import router as retrieve_router

# Import models so they're registered
from app.db import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(ingest_router)
app.include_router(chat_router)
app.include_router(retrieve_router)

@app.get("/health")
def health():

    postgres = False
    redis = False
    qdrant_ok = False

    try:
        with engine.connect():
            postgres = True
    except:
        pass

    try:
        redis_client.ping()
        redis = True
    except:
        pass

    try:
        qdrant.get_collections()
        qdrant_ok = True
    except:
        pass

    return {
        "postgres": postgres,
        "redis": redis,
        "qdrant": qdrant_ok,
    }