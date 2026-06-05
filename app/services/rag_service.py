from sqlalchemy.orm import Session

from app.services.llm_service import (
    generate_answer,
)
from app.services.retrieval_service import (
    retrieve_chunks,
)


def ask_question(
    db: Session,
    journal_id: int,
    question: str,
):

    results = retrieve_chunks(
        db=db,
        journal_id=journal_id,
        question=question,
        limit=5,
    )

    context = "\n\n".join(row.chunk_text for row in results)

    answer = generate_answer(
        question=question,
        context=context,
    )

    sources = []

    seen = set()

    for row in results:
        key = (
            row.journal_id,
            row.chunk_index,
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "journal_id": row.journal_id,
                "title": row.title,
                "chunk_index": row.chunk_index,
                "pdf_url": row.pdf_url,
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }
