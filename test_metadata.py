from app.services.llm_service import (
    extract_metadata_with_llm,
)
from app.services.pdf_service import (
    download_pdf,
    extract_text,
)

pdf = download_pdf("https://arxiv.org/pdf/1706.03762.pdf")

text = extract_text(pdf)

metadata = extract_metadata_with_llm(text)

print(metadata.model_dump())
