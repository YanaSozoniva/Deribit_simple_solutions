from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import settings
from app.db.basemodel import BaseORM
from app.postgres.price import Price  # noqa: F401 (нужен для alembic autogenerate)

# Alembic Config object
config = context.config

# Логирование из alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ВАЖНО: Используем sync_database_url для миграций
config.set_main_option("sqlalchemy.url", settings.sync_database_url)

# Метаданные для автогенерации
target_metadata = BaseORM.metadata


def run_migrations_offline() -> None:
    """Offline-режим: без подключения к БД, только генерация SQL."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online-режим: синхронное подключение к БД через psycopg2."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
