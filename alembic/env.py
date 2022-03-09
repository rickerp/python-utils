# pylint: disable=no-member
from __future__ import with_statement

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

config = context.config
assert config.config_file_name
fileConfig(config.config_file_name)


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=config.config_args.get("target_metadata"),
            user_module_prefix=""
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
