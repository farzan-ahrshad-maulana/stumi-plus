from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.repositories.journal_repository import (
    get_journal_by_id,
    get_journal_by_pdf_url,
    get_journals,
)
from app.schemas.journal import (
    JournalCreate,
)
from app.services.journal_service import create_journal
from app.services.llm_service import (
    extract_metadata_with_llm,
    validate_research_paper,
)
from app.services.metadata_service import (
    extract_metadata,
)
from app.services.pdf_service import (
    download_pdf,
    extract_text,
)
from app.services.validation_service import (
    basic_validation,
    validate_metadata,
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

    existing = get_journal_by_pdf_url(
        db=db,
        pdf_url=payload.pdf_url,
    )

    if existing:
        return {
            "id": existing.id,
            "title": existing.title,
            "status": "already_exists",
        }

    pdf_bytes = download_pdf(payload.pdf_url)

    text = extract_text(pdf_bytes)

    is_valid, error = basic_validation(text)

    if not is_valid:
        return {
            "status": "rejected",
            "reason": error,
        }

    metadata = extract_metadata_with_llm(text)

    validation = validate_research_paper(text)

    if not validation.is_research_paper or validation.confidence < 0.8:
        return {
            "status": "rejected",
            "reason": validation.reason,
            "confidence": validation.confidence,
        }

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


@router.get("/{journal_id}")
def get_journal(
    journal_id: int,
    db: Session = Depends(get_db),
):

    journal = get_journal_by_id(
        db,
        journal_id,
    )

    if not journal:
        return {"error": "Journal not found"}

    return {
        "id": journal.id,
        "title": journal.title,
        "authors": journal.authors,
        "institution": journal.institution,
        "abstract": journal.abstract,
        "pdf_url": journal.pdf_url,
    }
