from app.db.database import SessionLocal
from app.db.models import Journal
from app.services.embedding_service import (
    create_embedding,
)

db = SessionLocal()

journals = db.query(Journal).all()

for journal in journals:
    print(f"Updating journal {journal.id}")

    search_text = f"""
Title:
{journal.title}

Authors:
{journal.authors}

Abstract:
{journal.abstract}
"""

    journal.abstract_embedding = create_embedding(search_text)

db.commit()

print("Done")
