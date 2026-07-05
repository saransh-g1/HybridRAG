# scripts/test_repo.py

from app.db.session import SessionLocal
from app.repositories.document_repository import DocumentRepository

db = SessionLocal()

repo = DocumentRepository(db)

doc = repo.create(
    filename="sample.pdf",
    file_hash="12345",
)

db.commit()

print(doc.id)