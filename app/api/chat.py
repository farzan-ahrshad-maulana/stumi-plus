import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import logger
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
    try:
        start_time = time.time()
        logger.info(f"Question received for journal {payload.journal_id}")

        logger.info(f"Question: {payload.question}")

        result = ask_question(
            db=db,
            journal_id=payload.journal_id,
            question=payload.question,
        )

        duration = round(
            time.time() - start_time,
            2,
        )

        logger.info(f"Chat completed in {duration}s")

        return result

    except Exception as e:
        logger.exception("Chat request failed")

        return {
            "status": "error",
            "message": str(e),
        }
