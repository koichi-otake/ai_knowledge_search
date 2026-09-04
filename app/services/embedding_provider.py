from abc import ABC, abstractmethod

from openai import OpenAI
from sentence_transformers import SentenceTransformer

from app.core.config import settings


class EmbeddingProvider(ABC):

    @abstractmethod
    def create_embedding(
        self,
        text: str,
    ) -> list[float]:
        pass


class OpenAIEmbeddingProvider(
    EmbeddingProvider
):

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
        )

    def create_embedding(
        self,
        text: str,
    ) -> list[float]:

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return response.data[0].embedding


class MockEmbeddingProvider(
    EmbeddingProvider
):

    def create_embedding(
        self,
        text: str,
    ) -> list[float]:

        return [0.0] * settings.embedding_dimensions


class LocalEmbeddingProvider(
    EmbeddingProvider
):

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

    def create_embedding(
        self,
        text: str,
    ) -> list[float]:

        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()


def get_embedding_provider() -> EmbeddingProvider:

    if settings.embedding_provider == "openai":
        return OpenAIEmbeddingProvider()

    if settings.embedding_provider == "mock":
        return MockEmbeddingProvider()

    if settings.embedding_provider == "local":
        return LocalEmbeddingProvider()

    raise ValueError(
        "未対応のEmbedding Providerです: "
        f"{settings.embedding_provider}"
    )

