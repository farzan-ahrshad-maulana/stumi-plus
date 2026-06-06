from app.repositories.journal_repository import (
    semantic_search_journals,
)
from app.services.embedding_service import (
    create_embedding,
)


def search_journals(
    db,
    query: str,
    limit: int = 10,
):

    query_embedding = create_embedding(query)

    return semantic_search_journals(
        db=db,
        embedding=query_embedding,
        limit=limit,
    )
