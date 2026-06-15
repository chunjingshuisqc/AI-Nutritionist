from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI营养师Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 是否启用模拟大模型与模拟Embedding
    MOCK_MODE: bool = True

    DATABASE_URL: str = (
        "mysql+pymysql://root:password@localhost:3306/"
        "ai_nutritionist?charset=utf8mb4"
    )

    LLM_API_KEY: str = "mock-key"
    LLM_BASE_URL: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"

    EMBEDDING_API_KEY: str = "mock-key"
    EMBEDDING_BASE_URL: str = "https://api.openai.com/v1"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    CHROMA_PERSIST_DIR: str = "./knowledge_base"
    CHROMA_COLLECTION_NAME: str = "nutrition_knowledge"

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 5

    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()