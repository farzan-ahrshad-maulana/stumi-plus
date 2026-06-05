from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import (
    Chunk,
    Journal,
)

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
)


@router.get("/")
def get_stats(
    db: Session = Depends(get_db),
):

    journal_count = db.query(func.count(Journal.id)).scalar()

    chunk_count = db.query(func.count(Chunk.id)).scalar()

    return {
        "journals": journal_count,
        "chunks": chunk_count,
    }
