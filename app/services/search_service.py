from sqlalchemy.orm import Session

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

    return [
        {
            "chunk": row,
            "distance": row.distance,
        }
        for row in rows
    ]

