from app.core.config import settings
from app.services.embedding_provider import (
    get_embedding_provider,
)


provider = get_embedding_provider()


def create_embedding(
    text: str,
) -> list[float]:

    vector = provider.create_embedding(
        text=text,
    )

    if len(vector) != settings.embedding_dimensions:
        raise ValueError(
            "Embeddingの次元数が一致しません。"
            f" expected={settings.embedding_dimensions}"
            f" actual={len(vector)}"
        )

    return vector
