from app.services.search_service import search
from app.core.database import SessionLocal


db = SessionLocal()

results = search(
    db=db,
#   question="東京タワーは高さ何メートルですか？",
    question="有給休暇について教えてください",
    limit=7,
)

print("=" * 60)


for result in results:
    row = result["chunk"]

    print(f"id={row.id}")
    print(f"document={row.document_id}")
    print(f"chunk={row.chunk_index}")
    print(f"distance={result['distance']:.4f}")
    print(f"similarity={result['similarity']:.4f}")
    print(row.content[:100])
    print("-" * 60)


db.close()
