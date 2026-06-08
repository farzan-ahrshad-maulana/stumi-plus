import time

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.rate_limit import limiter
from app.db.dependencies import get_db
from app.repositories.journal_repository import (
    delete_journal,
    get_journal_by_id,
    get_journal_by_normalized_title_and_year,
    get_journal_by_pdf_url,
    #    get_journal_by_title_and_year,
    get_journals,
    hide_journal,
    unhide_journal,
)
from app.schemas.journal import (
    JournalCreate,
)
from app.schemas.search import (
    SearchRequest,
)
from app.services.journal_service import create_journal
from app.services.llm_service import (
    extract_metadata_with_llm,
)
from app.services.pdf_service import (
    download_pdf,
    extract_text,
)
from app.services.search_service import (
    search_journals,
)
from app.services.validation_service import (
    basic_validation,
    validate_metadata,
    validate_page_count,
    validate_pdf_size,
    validate_pdf_url,
    validate_text_pdf,
)
from app.services.vector_store_service import (
    store_chunks,
)

router = APIRouter(prefix="/journals", tags=["journals"])


@router.post("/")
@limiter.limit("5/minute")
def create_journal_endpoint(
    request: Request,
    payload: JournalCreate,
    db: Session = Depends(get_db),
):
    is_valid, reason = validate_pdf_url(
        payload.pdf_url,
    )

    if not is_valid:
        logger.warning(reason)

        return {
            "status": "rejected",
            "reason": reason,
        }
    try:
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
        is_valid, reason = validate_pdf_size(pdf_bytes)

        if not is_valid:
            logger.warning(reason)

            return {
                "status": "rejected",
                "reason": reason,
            }

        is_valid, reason = validate_page_count(pdf_bytes)

        if not is_valid:
            logger.warning(reason)

            return {
                "status": "rejected",
                "reason": reason,
            }

        is_valid, reason = validate_text_pdf(pdf_bytes)

        if not is_valid:
            logger.warning(reason)

            return {
                "status": "rejected",
                "reason": reason,
            }
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
        existing = get_journal_by_normalized_title_and_year(
            db=db,
            title=metadata.title,
            publication_year=metadata.publication_year,
        )

        if existing:
            logger.info(f"Duplicate paper detected: {existing.id}")

            return {
                "id": existing.id,
                "title": existing.title,
                "status": "already_exists",
            }

        logger.info(
            f"Metadata extraction took {round(time.time() - metadata_start, 2)}s"
        )

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

    except Exception:
        logger.exception("Journal ingestion failed")

        return {
            "status": "error",
            "message": "Internal server error",
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

    if not journal.is_public:
        return {"error": "Journal not found"}

    return {
        "id": journal.id,
        "title": journal.title,
        "authors": journal.authors,
        "institution": journal.institution,
        "abstract": journal.abstract,
        "pdf_url": journal.pdf_url,
    }


@router.patch("/{journal_id}/hide")
def hide_journal_endpoint(
    journal_id: int,
    db: Session = Depends(get_db),
):

    journal = get_journal_by_id(
        db,
        journal_id,
    )

    if not journal:
        return {"error": "Journal not found"}

    hide_journal(
        db,
        journal,
    )

    return {
        "id": journal.id,
        "status": "hidden",
    }


@router.patch("/{journal_id}/unhide")
def unhide_journal_endpoint(
    journal_id: int,
    db: Session = Depends(get_db),
):

    journal = get_journal_by_id(
        db,
        journal_id,
    )

    if not journal:
        return {"error": "Journal not found"}

    unhide_journal(
        db,
        journal,
    )

    return {
        "id": journal.id,
        "status": "public",
    }


@router.delete("/{journal_id}")
def delete_journal_endpoint(
    journal_id: int,
    db: Session = Depends(get_db),
):

    journal = get_journal_by_id(
        db,
        journal_id,
    )

    if not journal:
        return {"error": "Journal not found"}

    delete_journal(
        db,
        journal,
    )

    return {
        "id": journal_id,
        "status": "deleted",
    }


@router.post("/search")
@limiter.limit("30/minute")
def semantic_search_endpoint(
    request: Request,
    payload: SearchRequest,
    db: Session = Depends(get_db),
):

    results = search_journals(
        db=db,
        query=payload.query,
        limit=payload.limit,
    )

    return [
        {
            "id": row.id,
            "title": row.title,
            "authors": row.authors,
            "publication_year": row.publication_year,
            "pdf_url": row.pdf_url,
            "score": round(
                float(row.score),
                4,
            ),
        }
        for row in results
        #        if row.score > 0.50
    ]
