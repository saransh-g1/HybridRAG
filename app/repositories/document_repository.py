from app.db.models import Document


class DocumentRepository:

    def __init__(self, session):
        self.session = session

    def create(
        self,
        filename,
        file_hash,
    ):

        document = Document(
            filename=filename,
            file_hash=file_hash,
        )

        self.session.add(document)

        self.session.flush()

        return document

    def get_by_hash(
        self,
        file_hash,
    ):

        return (
            self.session.query(Document)
            .filter(
                Document.file_hash == file_hash
            )
            .first()
        )

    def get(
        self,
        document_id,
    ):

        return (
            self.session.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

    def delete(
        self,
        document,
    ):

        self.session.delete(document)