from sqlalchemy.orm import Session
import logging

from app.core.config import settings
from app.repositories.chunk_repository import search_by_embedding
from app.services.embedding_service import create_embedding

logger = logging.getLogger(__name__)

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

    logger.warning(
        "RAG検索: question=%s, threshold=%.3f, candidates=%d",
        question,
        settings.rag_similarity_threshold,
        len(rows),
    )

    results = []

    for row in rows:
        distance = float(row.distance)
        similarity = 1 - distance

        logger.warning(
            "RAG候補: chunk_id=%s document_id=%s distance=%.4f similarity=%.4f accepted=%s",
            row.id,
            row.document_id,
            distance,
            similarity,
            similarity >= settings.rag_similarity_threshold,
        )

        if similarity >= settings.rag_similarity_threshold:
            results.append(
                {
                    "chunk": row,
                    "distance": distance,
                    "similarity": similarity,
                }
            )

    return results
