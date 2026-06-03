# app/db/models.py

from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class Journal(Base):
    __tablename__ = "journals"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(500), nullable=False)

    authors: Mapped[str] = mapped_column(Text)

    institution: Mapped[str] = mapped_column(Text)

    journal_name: Mapped[str] = mapped_column(String(300))

    volume: Mapped[str] = mapped_column(String(50))

    publication_date: Mapped[Date] = mapped_column(Date)

    abstract: Mapped[str] = mapped_column(Text)

    pdf_url: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    chunks: Mapped[list["Chunk"]] = relationship(
        "Chunk", back_populates="journal", cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)

    journal_id: Mapped[int] = mapped_column(ForeignKey("journals.id"))

    chunk_text: Mapped[str] = mapped_column(Text)

    embedding: Mapped[list[float]] = mapped_column(Vector(768))

    chunk_index: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    journal: Mapped["Journal"] = relationship("Journal", back_populates="chunks")
