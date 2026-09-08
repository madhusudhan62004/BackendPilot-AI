from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    ENVIRONMENT: str

    MONGODB_URI: str
    DATABASE_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()