from pydantic import BaseSettings


class Settings(BaseSettings):
    # Secret key used for JWT token signing
    secret_key: str = "sua-chave-secreta-super-segura-aqui-mude-em-producao"
    # Algorithm used for JWT encoding
    algorithm: str = "HS256"
    # Token expiration time in minutes
    access_token_expire_minutes: int = 30
    # Async database connection URL
    database_url: str = "sqlite+aiosqlite:///./banking.db"

    class Config:
        # Load environment variables from .env file
        env_file = ".env"


# Global settings instance
settings = Settings()