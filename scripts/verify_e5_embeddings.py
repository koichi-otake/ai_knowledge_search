from app.core.database import SessionLocal
from app.repositories.chunk_repository import get_all_chunks
from app.services.embedding_service import create_embedding

db = SessionLocal()

try:
    chunks = get_all_chunks(db)
    print(f"対象チャンク数: {len(chunks)}")

    for chunk in chunks:
        vector = create_embedding(chunk.content, is_query=False)

        if len(vector) != 384:
            raise ValueError(
                f"chunk_id={chunk.id}: 次元数が不正です: {len(vector)}"
            )

        if not all(
            isinstance(value, (int, float))
            and value == value
            and abs(value) != float("inf")
            for value in vector
        ):
            raise ValueError(
                f"chunk_id={chunk.id}: ベクトルに不正な値があります"
            )

        print(
            f"chunk_id={chunk.id}: "
            f"次元数={len(vector)}, "
            f"旧ベクトルとの差分あり={vector != list(chunk.embedding or [])}"
        )

    print("検証完了。データベースは更新していません。")
finally:
    db.close()
