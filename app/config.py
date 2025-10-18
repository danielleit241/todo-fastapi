from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_HOST: str
    # POSTGRES_PORT: str
    # POSTGRES_DB: str
    CONNECTION_STRING: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = ConfigDict(
        extra="allow",
        env_file=".env"    
    )

settings = Settings()
