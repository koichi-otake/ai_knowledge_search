from app.core.database import SessionLocal
from app.services.search_service import search


db = SessionLocal()

results = search(
    db=db,
    question="有給休暇について教えてください",
    limit=5,
)

print("=" * 60)

for row in results:
    print(f"id={row.id}")
    print(f"document={row.document_id}")
    print(f"chunk={row.chunk_index}")
    print(f"distance={row.distance:.4f}")
    print(row.content[:100])
    print("-" * 60)

db.close()
