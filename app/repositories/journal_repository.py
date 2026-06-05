from sqlalchemy.orm import Session

from app.db.models import Journal


def get_journals(
    db: Session,
):
    return db.query(Journal).order_by(Journal.id.desc()).all()


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
