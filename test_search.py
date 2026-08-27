from app.core.database import SessionLocal
from app.repositories.chunk_repository import search_chunks

db = SessionLocal()

chunks = search_chunks(
    db=db,
)

print(len(chunks))

for chunk in chunks[:3]:
    print(chunk.id)
    print(chunk.content[:100])
