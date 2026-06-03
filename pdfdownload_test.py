from app.services.pdf_service import download_pdf

pdf_bytes = download_pdf(
    "https://arxiv.org/pdf/1706.03762.pdf"
)

print(len(pdf_bytes))
