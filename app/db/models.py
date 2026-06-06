# app/db/models.py

from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
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

    normalized_title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    authors: Mapped[str] = mapped_column(Text)

    institution: Mapped[str | None] = mapped_column(Text, nullable=True)
    journal_name: Mapped[str | None] = mapped_column(String(300), nullable=True)

    volume: Mapped[str | None] = mapped_column(String(50), nullable=True)
    publication_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    publication_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    abstract_embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1024),
        nullable=True,
    )

    abstract: Mapped[str] = mapped_column(Text)

    pdf_url: Mapped[str] = mapped_column(Text)

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    chunks: Mapped[list["Chunk"]] = relationship(
        "Chunk", back_populates="journal", cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)

    journal_id: Mapped[int] = mapped_column(ForeignKey("journals.id"))

    chunk_text: Mapped[str] = mapped_column(Text)

    embedding: Mapped[list[float]] = mapped_column(Vector(1024))

    chunk_index: Mapped[int]

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    journal: Mapped["Journal"] = relationship("Journal", back_populates="chunks")
