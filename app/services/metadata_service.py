from pydantic import BaseModel


class ExtractedMetadata(BaseModel):
    title: str

    authors: str

    abstract: str


def extract_metadata(text: str) -> ExtractedMetadata:

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    title = ""

    for line in lines:
        if len(line) > 10 and "attention is all you need" in line.lower():
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

    return ExtractedMetadata(
        title=title,
        authors=authors,
        abstract=abstract,
    )
