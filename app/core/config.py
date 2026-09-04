from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    app_name: str = "AI社内ナレッジ検索システム"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str
    openai_api_key: str

    rag_similarity_threshold: float = 0.75
    embedding_provider: str = "mock"
    embedding_dimensions: int = 384

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
