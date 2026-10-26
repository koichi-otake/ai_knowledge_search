from app.core.database import SessionLocal
from app.repositories.chunk_repository import search_similar_chunks
from app.services.embedding_service import create_embedding


db = SessionLocal()

try:
    #question = "有給休暇はいつ何日付与されますか？"
    #question = "どのような仕事をしてきましたか？"
    question = "次世代光ディスクやCMOSイメージセンサの研究開発、製品設計について教えてください"

    query_embedding = create_embedding(question, is_query=True)

    chunks = search_similar_chunks(
        db=db,
        query_embedding=query_embedding,
        limit=20,
    )

    print("検索結果:", len(chunks))

    for result in chunks:
        chunk, distance = result

        print()
        print("id:", chunk.id)
        print("document_id:", chunk.document_id)
        print("chunk_index:", chunk.chunk_index)
        print("content:", chunk.content[:100])
        print("distance:", distance)

finally:
    db.close()
