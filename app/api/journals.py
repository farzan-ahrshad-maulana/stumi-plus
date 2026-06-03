from fastapi import APIRouter

from app.schemas.journal import (
    JournalCreate,
)

router = APIRouter()


@router.post("/journals")
def create_journal(
    payload: JournalCreate,
):

    return {"pdf_url": payload.pdf_url}
