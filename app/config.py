from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    database_url: str

    # Supabase
    supabase_url: str
    supabase_key: str
    supabase_bucket: str = "files"

    # Configuración de archivos
    max_file_size_mb: int = 100
    expiration_hours: int = 72

    class Config:
        env_file = ".env"


settings = Settings()
