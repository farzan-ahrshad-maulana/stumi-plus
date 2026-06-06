from sqlalchemy.orm import Session

from app.db.models import Journal
from app.services.metadata_service import (
    normalize_title,
)


def get_journals(
    db: Session,
):
    return (
        db.query(Journal)
        .filter(Journal.is_public == True)
        .order_by(Journal.id.desc())
        .all()
    )


def get_journal_by_id(
    db: Session,
    journal_id: int,
):
    return db.query(Journal).filter(Journal.id == journal_id).first()


def get_journal_by_pdf_url(
    db: Session,
    pdf_url: str,
):
    return db.query(Journal).filter(Journal.pdf_url == pdf_url).first()


def get_journal_by_title_and_year(
    db: Session,
    title: str,
    publication_year: int,
):

    return (
        db.query(Journal)
        .filter(
            Journal.title == title,
            Journal.publication_year == publication_year,
        )
        .first()
    )


def get_journal_by_normalized_title_and_year(
    db: Session,
    title: str,
    publication_year: int,
):

    normalized_title = normalize_title(title)

    return (
        db.query(Journal)
        .filter(
            Journal.normalized_title == normalized_title,
            Journal.publication_year == publication_year,
        )
        .first()
    )


def hide_journal(
    db: Session,
    journal: Journal,
):

    journal.is_public = False

    db.commit()

    db.refresh(journal)

    return journal


def unhide_journal(
    db: Session,
    journal: Journal,
):

    journal.is_public = True

    db.commit()

    db.refresh(journal)

    return journal


def delete_journal(
    db: Session,
    journal: Journal,
):

    db.delete(journal)

    db.commit()
