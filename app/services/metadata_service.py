import re

from pydantic import BaseModel


class ExtractedMetadata(BaseModel):
    title: str

    authors: str

    institution: str

    abstract: str


def extract_metadata(text: str) -> ExtractedMetadata:

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    title = ""

    for line in lines[:20]:
        if (
            len(line) > 10
            and len(line) < 200
            and "abstract" not in line.lower()
            and "provided proper attribution" not in line.lower()
            and "reproduce the tables" not in line.lower()
        ):
            title = line
            break

    if not title:
        title = lines[0]

    authors = ""

    try:
        title_index = lines.index(title)

        authors = lines[title_index + 1]

    except Exception:
        authors = ""

    abstract = ""

    for i, line in enumerate(lines):
        if line.lower() == "abstract":
            abstract = " ".join(lines[i + 1 : i + 10])

            break

    institution = ""
    return ExtractedMetadata(
        title=title,
        authors=authors,
        institution=institution,
        abstract=abstract,
    )


def normalize_title(
    title: str,
) -> str:

    title = title.lower()

    title = re.sub(
        r"[^\w\s]",
        " ",
        title,
    )

    title = " ".join(title.split())

    return title
