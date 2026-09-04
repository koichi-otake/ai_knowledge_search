from sqlalchemy.orm import Session

from app.models.chunk import ChunkORM

from sqlalchemy import select

from sqlalchemy import text

def create_chunk(
    db: Session,
    document_id: int,
    chunk_index: int,
    content: str,
) -> ChunkORM:

    chunk = ChunkORM(
        document_id=document_id,
        chunk_index=chunk_index,
        content=content,
    )

    db.add(chunk)

    return chunk

def create_chunks(
    db: Session,
    document_id: int,
    chunks: list[str],
    embeddings: list[list[float]],
) -> list[ChunkORM]:

    results = []

    for index, (content, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        chunk = ChunkORM(
            document_id=document_id,
            chunk_index=index,
            content=content,
            embedding=embedding,
        )

        db.add(chunk)
        results.append(chunk)

    return results

def search_chunks(
    db: Session,
):
    stmt = select(
        ChunkORM
    )

    return db.scalars(stmt).all()


def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    limit: int = 5,
) -> list[tuple[ChunkORM, float]]:

    distance = ChunkORM.embedding.cosine_distance(
        query_embedding
    )

    statement = (
        select(
            ChunkORM,
            distance.label("distance"),
        )
        .where(ChunkORM.embedding.is_not(None))
        .order_by(distance)
        .limit(limit)
    )

    rows = db.execute(statement).all()

    return [
        (chunk, float(distance_value))
        for chunk, distance_value in rows
    ]


def search_by_embedding(
    db,
    embedding: list[float],
    limit: int = 5,
):
    sql = text("""
        SELECT
            id,
            document_id,
            chunk_index,
            content,
            created_at,
            embedding <=> CAST(:embedding AS vector) AS distance
        FROM chunks
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "embedding": embedding,
            "limit": limit,
        },
    )

    return result.fetchall()




def update_embedding(
    db,
    chunk_id: int,
    embedding: list[float],
):
    chunk = db.get(
        ChunkORM,
        chunk_id,
    )

    if chunk is None:
        return

    chunk.embedding = embedding

    db.commit()



def get_all_chunks(db):
    return db.scalars(
        select(ChunkORM)
    ).all()
