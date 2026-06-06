from sqlalchemy.orm import Session

from app.db.models import Journal
from app.schemas.metadata import LLMMetadata
from app.services.embedding_service import (
    create_embedding,
)
from app.services.metadata_service import (
    normalize_title,
)


def create_journal(
    db: Session,
    metadata: LLMMetadata,
    pdf_url: str,
) -> Journal:
    normalized_title = normalize_title(metadata.title)

    search_text = f"""
    Title:
    {metadata.title}

    Authors:
    {metadata.authors}

    Abstract:
    {metadata.abstract}
    """

    abstract_embedding = create_embedding(search_text)

    journal = Journal(
        title=metadata.title,
        normalized_title=normalized_title,
        authors=metadata.authors,
        institution=metadata.institution,
        publication_year=metadata.publication_year,
        abstract=metadata.abstract,
        abstract_embedding=abstract_embedding,
        pdf_url=pdf_url,
    )

    db.add(journal)

    db.commit()

    db.refresh(journal)

    return journal
