from app.services.embedding_service import create_embedding

vector = create_embedding(
    "今日は晴れです。"
)

print(type(vector))
print(len(vector))
print(vector[:10])
