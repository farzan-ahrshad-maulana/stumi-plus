from app.core.logger import logger
from app.schemas.metadata import LLMMetadata


def basic_validation(
    text: str,
) -> tuple[bool, str]:

    is_valid, reason = academic_structure_validation(text)

    if not is_valid:
        logger.warning(reason)
        return {
            "status": "rejected",
            "reason": reason,
        }

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


def academic_structure_validation(
    text: str,
) -> tuple[bool, str]:

    text_lower = text.lower()

    keywords = [
        "abstract",
        "introduction",
        "references",
    ]

    found = sum(1 for keyword in keywords if keyword in text_lower)

    if found < 2:
        return (
            False,
            "Document does not appear to be an academic paper",
        )

    return True, ""
