from app.db.database import SessionLocal
from app.services.retrieval_service import (
    retrieve_chunks,
)

db = SessionLocal()

results = retrieve_chunks(
    db=db,
    question="What is the Transformer architecture?",
)

for row in results:
    print("=" * 80)

    print("Distance:", row.distance)

    print()

    print(row.chunk_text[:500])
