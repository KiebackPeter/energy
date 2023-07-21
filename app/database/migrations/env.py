from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic.context import (
    config,
    configure,
    begin_transaction,
    run_migrations,
    is_offline_mode,
)
from app.core.settings import env

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name:
    fileConfig(config.config_file_name)


# add your model's MetaData object here
# for 'autogenerate' support
from app.database.models.base import BaseModel  # pylint: disable=wrong-import-position

target_metadata = BaseModel.metadata
database_url = env.DB.url + env.DB.name

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with begin_transaction():
        run_migrations()


def run_migrations_online() -> None:
    """Run migrations against the database."""
    connectable = engine_from_config(
        configuration={
            "prefix": "sqlalchemy",
            "poolclass": pool.NullPool,
        },
        url=database_url,
    )

    with connectable.connect() as connection:
        configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)

        with begin_transaction():
            run_migrations()


if is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
