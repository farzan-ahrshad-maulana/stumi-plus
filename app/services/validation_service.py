from app.schemas.metadata import LLMMetadata


def basic_validation(
    text: str,
) -> tuple[bool, str]:

    if not text.strip():
        return False, "PDF contains no extractable text"

    if len(text) < 5000:
        return False, "Document too short"

    if len(text.split()) < 1000:
        return False, "Not enough words"

    return True, ""


def validate_metadata(
    metadata: LLMMetadata,
) -> tuple[bool, str]:

    if len(metadata.title.strip()) < 10:
        return False, "Invalid title"

    if len(metadata.authors.strip()) < 5:
        return False, "Invalid authors"

    if len(metadata.abstract.strip()) < 300:
        return False, "Abstract too short"

    return True, ""
