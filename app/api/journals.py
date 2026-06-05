from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.journal_repository import (
    get_journals,
)
from app.schemas.journal import (
    JournalCreate,
)
from app.services.journal_service import create_journal
from app.services.llm_service import (
    extract_metadata_with_llm,
)
from app.services.metadata_service import (
    extract_metadata,
)
from app.services.pdf_service import (
    download_pdf,
    extract_text,
)
from app.services.vector_store_service import (
    store_chunks,
)

router = APIRouter(prefix="/journals", tags=["journals"])


@router.post("/")
def create_journal_endpoint(
    payload: JournalCreate,
    db: Session = Depends(get_db),
):

    pdf_bytes = download_pdf(payload.pdf_url)

    text = extract_text(pdf_bytes)

    metadata = extract_metadata_with_llm(text)

    journal = create_journal(
        db=db,
        metadata=metadata,
        pdf_url=payload.pdf_url,
    )

    chunk_count = store_chunks(
        db=db,
        journal_id=journal.id,
        text=text,
    )

    return {
        "id": journal.id,
        "title": journal.title,
        "chunks": chunk_count,
        "status": "saved",
    }


@router.get("/")
def list_journals(
    db: Session = Depends(get_db),
):

    journals = get_journals(db)

    return [
        {
            "id": journal.id,
            "title": journal.title,
            "authors": journal.authors,
            "pdf_url": journal.pdf_url,
        }
        for journal in journals
    ]
