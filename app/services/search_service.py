from sqlalchemy.orm import Session
from app.core.config import settings
from app.repositories.chunk_repository import search_similar_chunks
from app.services.embedding_service import create_embedding


def search(
    db: Session,
    question: str,
    limit: int = 5,
):
    query_embedding = create_embedding(
        question
    )

    results = search_similar_chunks(
        db=db,
        query_embedding=query_embedding,
        limit=limit,
    )

    relevant_chunks = []

    for chunk, distance in results:
        similarity = 1.0 - distance

        if similarity >= settings.rag_similarity_threshold:
            relevant_chunks.append(
                {
                    "chunk": chunk,
                    "similarity": similarity,
                }
            )

    return relevant_chunks
