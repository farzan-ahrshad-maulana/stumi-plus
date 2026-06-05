import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
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
    try:

        logger.info(
            f"New journal submission: {payload.pdf_url}"
        )

        ...
        seluruh kode existing ...

        return {
            "id": journal.id,
            "title": journal.title,
            "chunks": chunk_count,
            "status": "saved",
        }

    except Exception as e:

        logger.exception(
            "Journal ingestion failed"
        )

        return {
            "status": "error",
            "message": str(e),
        }
    logger.info(f"New journal submission: {payload.pdf_url}")

    start_time = time.time()
    existing = get_journal_by_pdf_url(
        db=db,
        pdf_url=payload.pdf_url,
    )

    if existing:
        logger.info(f"Duplicate journal detected: {existing.id}")
        return {
            "id": existing.id,
            "title": existing.title,
            "status": "already_exists",
        }

    pdf_bytes = download_pdf(payload.pdf_url)
    logger.info(f"PDF downloaded ({len(pdf_bytes)} bytes)")

    text = extract_text(pdf_bytes)
    logger.info(f"Text extracted successfully ({len(text)} chars)")

    is_valid, reason = basic_validation(text)

    if not is_valid:
        logger.warning(f"Basic validation failed: {reason}")

        return {
            "status": "rejected",
            "reason": reason,
        }

    logger.info("Basic validation passed")

    metadata_start = time.time()
    metadata = extract_metadata_with_llm(text)
    logger.info(f"Metadata extraction took {round(time.time() - metadata_start, 2)}s")

    logger.info(f"Metadata extracted: {metadata.title}")

    is_valid, reason = validate_metadata(metadata)

    if not is_valid:
        logger.warning(f"Metadata validation failed: {reason}")

        return {
            "status": "rejected",
            "reason": reason,
        }

    logger.info("Metadata validation passed")

    journal = create_journal(
        db=db,
        metadata=metadata,
        pdf_url=payload.pdf_url,
    )
    logger.info(f"Journal saved: {journal.id}")

    embedding_start = time.time()
    chunk_count = store_chunks(
        db=db,
        journal_id=journal.id,
        text=text,
    )
    logger.info(f"Embedding stage took {round(time.time() - embedding_start, 2)}s")
    logger.info(f"Stored {chunk_count} chunks for journal {journal.id}")

    duration = round(
        time.time() - start_time,
        2,
    )

    logger.info(f"Journal {journal.id} ingestion completed in {duration}s")
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
