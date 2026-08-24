from sqlalchemy.orm import Session

from app.models.chunk import ChunkORM


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
) -> list[ChunkORM]:

    results = []

    for index, content in enumerate(chunks):

        chunk = ChunkORM(
            document_id=document_id,
            chunk_index=index,
            content=content,
        )

        db.add(chunk)

        results.append(chunk)

    return results
