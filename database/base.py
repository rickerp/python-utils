from abc import ABC, abstractmethod
from typing import Generator

from pydantic import PostgresDsn


class Database(ABC):
    def __init__(self, user: str, password: str, host: str, port: str, name: str):
        self.database_uri = PostgresDsn.build(
            scheme="postgresql",
            user=user,
            password=password,
            host=host,
            port=port,
            path=f"/{name or ''}",
        )

    @abstractmethod
    def session(self):
        pass

    def get_db(self) -> Generator:
        # https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-tables
        db = self.session()
        try:
            yield db
        finally:
            db.close()
