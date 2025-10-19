from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str | None = "My FastAPI Project"
    API_PREFIX: str | None = "/api/v1"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int | None = 30

    model_config = ConfigDict(
        extra="allow",
        env_file='.env',
        env_file_encoding="utf-8",   
    )

settings = Settings()
