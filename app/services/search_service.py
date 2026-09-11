from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.chunk_repository import search_by_embedding
from app.services.embedding_service import create_embedding


def search(
    db: Session,
    question: str,
    limit: int = 5,
):
    embedding = create_embedding(question)

    rows = search_by_embedding(
        db=db,
        embedding=embedding,
        limit=limit,
    )

    results = []

    for row in rows:
        distance = float(row.distance)
        similarity = 1 - distance

        if similarity >= settings.rag_similarity_threshold:
            results.append(
                {
                    "chunk": row,
                    "distance": distance,
                    "similarity": similarity,
                }
            )

    return results
