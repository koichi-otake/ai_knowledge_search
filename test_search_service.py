from app.core.database import SessionLocal
from app.services.search_service import search


db = SessionLocal()

try:
    results = search(
        db=db,
        question="有給休暇は何日ですか？",
        limit=5,
    )

    print("検索結果:", len(results))

    for chunk in results:
        print()
        print("id:", chunk.id)
        print("document_id:", chunk.document_id)
        print("chunk_index:", chunk.chunk_index)
        print("content:", chunk.content[:100])

finally:
    db.close()
