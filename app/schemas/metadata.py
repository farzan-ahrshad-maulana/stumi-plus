from pydantic import BaseModel


class LLMMetadata(BaseModel):
    title: str
    authors: str
    institution: str
    abstract: str
    publication_year: int | None = None
