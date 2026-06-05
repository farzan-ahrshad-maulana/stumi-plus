from sqlalchemy.orm import Session

from app.db.models import Journal


def get_journals(
    db: Session,
):
    return db.query(Journal).order_by(Journal.id.desc()).all()
