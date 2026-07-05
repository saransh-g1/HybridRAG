from app.db.models import Chunk


class ChunkRepository:

    def __init__(self, session):
        self.session = session

    def get_by_id(self, chunk_id: int):
        return (
            self.session.query(Chunk)
            .filter(Chunk.id == chunk_id)
            .first()
        )


    def get_by_ids(self, ids: list[int]):

        chunks = (
            self.session.query(Chunk)
            .filter(Chunk.id.in_(ids))
            .all()
        )

        lookup = {
            chunk.id: chunk
            for chunk in chunks
        }

        return [
            lookup[i]
            for i in ids
            if i in lookup
        ]

    def create(
        self,
        document_id,
        chunk_index,
        page,
        text,
    ):

        chunk = Chunk(
            document_id=document_id,
            chunk_index=chunk_index,
            page=page,
            text=text,
        )

        self.session.add(chunk)

        self.session.flush()

        return chunk

    def get(
        self,
        chunk_id,
    ):

        return (
            self.session.query(Chunk)
            .filter(
                Chunk.id == chunk_id
            )
            .first()
        )

    def get_all(self):

        return (
            self.session.query(Chunk)
            .all()
        )

    def get_by_document(
        self,
        document_id,
    ):

        return (
            self.session.query(Chunk)
            .filter(
                Chunk.document_id == document_id
            )
            .all()
        )

    def delete(
        self,
        chunk,
    ):

        self.session.delete(chunk)