from dataclasses import dataclass

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


@dataclass
class TextChunk:
    text: str
    index: int


def chunk_text(text: str) -> list[TextChunk]:

    chunks: list[TextChunk] = []

    start = 0
    index = 0

    while start < len(text):
        end = start + CHUNK_SIZE

        chunk = text[start:end]

        chunks.append(
            TextChunk(
                text=chunk,
                index=index,
            )
        )

        start += CHUNK_SIZE - CHUNK_OVERLAP

        index += 1

    return chunks
