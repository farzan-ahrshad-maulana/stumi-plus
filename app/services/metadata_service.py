from pydantic import BaseModel


class ExtractedMetadata(BaseModel):
    title: str

    authors: str

    abstract: str


def extract_metadata(
    text: str,
) -> ExtractedMetadata:

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    title = lines[0]

    authors = lines[1]

    abstract = ""

    abstract_index = None

    for i, line in enumerate(lines):
        if "abstract" in line.lower():
            abstract_index = i

            break

    if abstract_index:
        abstract = " ".join(lines[abstract_index : abstract_index + 10])

    return ExtractedMetadata(
        title=title,
        authors=authors,
        abstract=abstract,
    )
