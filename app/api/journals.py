from fastapi import APIRouter

from app.schemas.journal import (
    JournalCreate,
)
from app.services.metadata_service import (
    extract_metadata,
)
from app.services.pdf_service import (
    download_pdf,
    extract_text,
)

router = APIRouter(prefix="/journals", tags=["journals"])


@router.post("/")
def create_journal(payload: JournalCreate):

    pdf_bytes = download_pdf(payload.pdf_url)

    text = extract_text(pdf_bytes)
    print("=" * 50)
    print(text[:5000])
    print("=" * 50)

    metadata = extract_metadata(text)

    return metadata
