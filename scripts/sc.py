from app.db.base import Base
from app.db.session import engine

import app.db.models

Base.metadata.create_all(bind=engine)

print("Database initialized.")