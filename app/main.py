from fastapi import FastAPI
from sqlalchemy import text

from app.api.chat import (
    router as chat_router,
)
from app.api.journals import router as journal_router
from app.api.stats import (
    router as stats_router,
)
from app.db.database import engine

app = FastAPI(title="Stumi", version="0.1.0")
app.include_router(journal_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "Welcome to Stumi Research Assitant"}


@app.get("/health")
def health():

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }
