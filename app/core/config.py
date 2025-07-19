from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_NAME: str = "recipe_book"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    SECRET_KEY: str = "31d6cfe0d16ae931b73c59d7e0c089c0"
    ALGORITHM: str = "HS256"

settings = Settings()

def get_gb_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")