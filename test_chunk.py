from app.services.chunk_service import split_text
from app.services.pdf_service import extract_text


text = extract_text(
    "storage/documents/20260130_履歴書_小竹晃一.pdf"
#   "storage/documents/sample.pdf"
)

chunks = split_text(
    text,
    chunk_size=500,
    chunk_overlap=100,
)

print("チャンク数:", len(chunks))

for index, chunk in enumerate(chunks[:3]):
    print()
    print(f"--- chunk {index} ---")
    print(chunk)
