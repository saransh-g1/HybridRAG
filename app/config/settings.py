from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str

    HOST: str
    PORT: int

    LLM_PROVIDER: str

    LLM_API_KEY: str

    LLM_BASE_URL: str

    LLM_MODEL: str

    EMBEDDING_PROVIDER: str

    EMBEDDING_MODEL: str

    POSTGRES_URL: str

    REDIS_URL: str

    QDRANT_URL: str

    QDRANT_COLLECTION: str

    USE_HYDE: bool = False

    class Config:
        env_file = ".env"


settings = Settings()