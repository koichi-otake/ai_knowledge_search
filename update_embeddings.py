from app.core.database import SessionLocal
from app.repositories.chunk_repository import (
    get_all_chunks,
    update_embedding,
)
from app.services.embedding_service import create_embedding


def main():
    db = SessionLocal()

    chunks = get_all_chunks(db)

    print(f"{len(chunks)}件のチャンクを更新します")

    for chunk in chunks:
        print(f"Chunk {chunk.id} を更新中...")

        embedding = create_embedding(
            chunk.content,
        )

        update_embedding(
            db=db,
            chunk_id=chunk.id,
            embedding=embedding,
        )

    db.close()

    print("完了しました。")


if __name__ == "__main__":
    main()
