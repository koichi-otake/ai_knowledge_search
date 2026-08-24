from app.services.pdf_service import extract_text

text = extract_text(
#   "storage/documents/sample.pdf"
    "storage/documents/20260130_職務経歴書_小竹晃一.pdf"
)


print(text)
