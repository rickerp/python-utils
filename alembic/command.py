import os
from time import time
from typing import Any, Optional

from pydantic import PostgresDsn

from alembic import command
from alembic.config import Config


class Alembic:
    def __init__(self, *, database_uri: PostgresDsn, migrations_location: str, model_metadata: Any):
        self.alembic_cfg = Config(
            file_=os.path.join(os.path.dirname(__file__), "alembic.ini"),
            config_args={"target_metadata": model_metadata},  # type: ignore
        )
        self.alembic_cfg.set_main_option("script_location", os.path.dirname(__file__))
        self.alembic_cfg.set_main_option("version_locations", migrations_location)

        db_uri = database_uri.replace('%', '%%')
        # https://alembic.sqlalchemy.org/en/latest/api/config.html#alembic.config.Config.set_main_option
        # A raw percent sign not part of an interpolation symbol must therefore be escaped
        self.alembic_cfg.set_main_option("sqlalchemy.url", db_uri)

    def run_revision(self, message: Optional[str] = None):
        command.revision(self.alembic_cfg, autogenerate=True, message=message, rev_id=str(int(time())))

    def run_upgrade(self, revision: str = "head"):
        command.upgrade(self.alembic_cfg, revision)

    def run_downgrade(self, revision: str):
        command.downgrade(self.alembic_cfg, revision)

    def run(self, cmd: str, *args, **kwargs):
        getattr(command, cmd)(self.alembic_cfg, *args, **kwargs)
