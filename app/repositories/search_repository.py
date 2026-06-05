from sqlalchemy import text
from sqlalchemy.orm import Session


def search_chunks(
    db: Session,
    embedding: list[float],
    limit: int = 5,
):

    query = text(
        """
        SELECT
            c.id,
            c.journal_id,
            c.chunk_index,
            c.chunk_text,
            j.title,
            embedding <=> CAST(:embedding AS vector)
                AS distance
        FROM chunks c
        JOIN journals j
            ON c.journal_id = j.id
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
        """
    )

    result = db.execute(
        query,
        {
            "embedding": str(embedding),
            "limit": limit,
        },
    )

    return result.fetchall()
