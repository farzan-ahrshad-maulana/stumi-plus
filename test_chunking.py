from app.services.chunking_service import (
    chunk_text,
)
from app.services.pdf_service import (
    download_pdf,
    extract_text,
)

pdf = download_pdf("https://arxiv.org/pdf/1706.03762.pdf")

text = extract_text(pdf)

chunks = chunk_text(text)

print("Total chunks:", len(chunks))

print()

print("Chunk 0:")
print(chunks[0].text[:300])

print()

print("Chunk 1:")
print(chunks[1].text[:300])
