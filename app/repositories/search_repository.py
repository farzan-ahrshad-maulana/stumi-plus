from sqlalchemy import text
from sqlalchemy.orm import Session


def search_chunks(
    db: Session,
    embedding: list[float],
    journal_id: int,
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
            j.pdf_url,
            embedding <=> CAST(:embedding AS vector)
                AS distance
        FROM chunks c
        JOIN journals j
            ON c.journal_id = j.id
        WHERE c.journal_id = :journal_id
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
        """
    )

    result = db.execute(
        query,
        {
            "embedding": str(embedding),
            "journal_id": journal_id,
            "limit": limit,
        },
    )

    return result.fetchall()
