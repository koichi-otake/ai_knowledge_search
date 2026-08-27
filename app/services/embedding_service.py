from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.openai_api_key,
)


def create_embedding(text: str) -> list[float]:
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )
        return response.data[0].embedding

    except APIError as e:
        raise RuntimeError(
            f"Embeddingの生成に失敗しました: {e}"
        ) from e
