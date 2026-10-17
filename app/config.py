from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Crypto Tracker API"
    app_version: str = "0.1.0"
    debug: bool = False

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "deribit_db"
    db_echo: bool = False

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    celery_interval_seconds: int = 60

    deribit_base_url: str = "https://www.deribit.com/api/v2"
    deribit_timeout_seconds: int = 10
    tracked_tickers: list[str] = Field(default_factory=lambda: ["BTC", "ETH"])

    @computed_field
    @property
    def database_url(self) -> str:
        """Async URL для приложения."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def sync_database_url(self) -> str:
        """Sync URL для Alembic (используем современный psycopg v3)"""
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def celery_broker_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    @computed_field
    @property
    def celery_result_backend(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db + 1}"


settings = Settings()
