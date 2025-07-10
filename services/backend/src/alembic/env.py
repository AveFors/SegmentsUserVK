import asyncio
from logging.config import fileConfig
from alembic import context

from sqlalchemy import pool
from sqlalchemy.engine import Connection


from core.config import settings
from core.models.base import Base
from core import models  # важно для регистрации всех моделей


from core.models.db_helper import db_helper


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


config.set_main_option("sqlalchemy.url", settings.db.url)


target_metadata = Base.metadata


# --- OFFLINE MODE (чаще не используется с async) ---
def run_migrations_offline():
    """Запускает миграции без подключения к БД."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# --- ONLINE MODE ---
def run_migrations_online():
    """Запускает миграции с подключением к БД через db_helper.engine."""

    async def do_run_migrations():
        async with db_helper.engine.connect() as connection:
            await connection.run_sync(run_migrations)

    def run_migrations(connection: Connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations())



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
