from app.core.database import SessionLocal
from app.repositories.chunk_repository import get_all_chunks
from app.services.embedding_service import create_embedding


def main():
    db = SessionLocal()

    try:
        chunks = get_all_chunks(db)

        if not chunks:
            print("対象チャンクがありません。")
            return

        print(f"更新対象: {len(chunks)}件")

        new_embeddings = []

        for chunk in chunks:
            embedding = create_embedding(
                chunk.content,
                is_query=False,
            )

            if len(embedding) != 384:
                raise ValueError(
                    f"chunk_id={chunk.id}: "
                    f"次元数が不正です: {len(embedding)}"
                )

            new_embeddings.append((chunk, embedding))

        print("\n更新対象のチャンクID:")
        print([chunk.id for chunk, _ in new_embeddings])

        confirmation = input(
            "E5ベクトルで更新しますか？ (yes と入力): "
        )

        if confirmation != "yes":
            print("更新をキャンセルしました。")
            return

        # 全件のベクトル生成が成功し、確認された場合のみ更新
        for chunk, embedding in new_embeddings:
            chunk.embedding = embedding

        db.commit()
        print(f"更新完了: {len(new_embeddings)}件")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
