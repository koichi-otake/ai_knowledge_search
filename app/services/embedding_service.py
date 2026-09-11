from functools import lru_cache

from app.core.config import settings
from app.services.embedding_provider import (
    get_embedding_provider,
)


@lru_cache
def get_provider():
    return get_embedding_provider()


def create_embedding(
    text: str,
) -> list[float]:

    provider = get_provider()

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
