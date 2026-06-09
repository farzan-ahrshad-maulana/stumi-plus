# Stumi Plus v1.0.0

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text

from app.api.chat import (
    router as chat_router,
)
from app.api.journals import router as journal_router
from app.api.stats import (
    router as stats_router,
)
from app.core.logger import logger
from app.core.rate_limit import limiter
from app.db.database import engine

app = FastAPI(
    title="Stumi",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ratetest")
@limiter.limit("3/minute")
def ratetest(request: Request):
    return {"ok": True}


app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(SlowAPIMiddleware)

app.include_router(journal_router)
app.include_router(chat_router)
app.include_router(stats_router)


@app.get("/")
def root():
    return {"message": "Welcome to Stumi Research Assitant"}


@app.on_event("startup")
def startup():

    logger.info("Stumi API started successfully")


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
