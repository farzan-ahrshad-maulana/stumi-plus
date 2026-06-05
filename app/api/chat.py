from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import (
    ChatRequest,
)
from app.services.rag_service import (
    ask_question,
)

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/")
def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
):

    result = ask_question(
        db=db,
        journal_id=payload.journal_id,
        question=payload.question,
    )

    return result
