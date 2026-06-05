from sqlalchemy.orm import Session

from app.repositories.search_repository import (
    search_chunks,
)
from app.services.embedding_service import (
    create_embedding,
)


def retrieve_chunks(
    db: Session,
    question: str,
    limit: int = 5,
):

    question_embedding = create_embedding(question)

    results = search_chunks(
        db=db,
        embedding=question_embedding,
        limit=limit,
    )

    return results
