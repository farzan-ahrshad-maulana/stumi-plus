from sqlalchemy.orm import Session

from app.db.models import Journal
from app.schemas.metadata import LLMMetadata


def create_journal(
    db: Session,
    metadata: LLMMetadata,
    pdf_url: str,
) -> Journal:

    journal = Journal(
        title=metadata.title,
        authors=metadata.authors,
        institution=metadata.institution,
        abstract=metadata.abstract,
        pdf_url=pdf_url,
    )

    db.add(journal)

    db.commit()

    db.refresh(journal)

    return journal
