from app.core.database import SessionLocal
from app.repositories.chunk_repository import search_similar_chunks


db = SessionLocal()

try:
    query_embedding = [0.0] * 1536

    chunks = search_similar_chunks(
        db=db,
        query_embedding=query_embedding,
        limit=5,
    )

    print("検索結果:", len(chunks))

    for chunk in chunks:
        print()
        print("id:", chunk.id)
        print("document_id:", chunk.document_id)
        print("chunk_index:", chunk.chunk_index)
        print("content:", chunk.content[:100])

finally:
    db.close()
