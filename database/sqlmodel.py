from typing import Union

from sqlalchemy.orm import Session as SASession
from sqlmodel import Session, SQLModel, create_engine

from utils.string import camel_to_snake_case

from .base import Database


class SQLModelDatabase(Database):
    def __init__(self, user: str, password: str, host: str, port: str, name: str):
        super().__init__(user, password, host, port, name)
        self.engine = create_engine(self.database_uri, pool_pre_ping=True)

    def session(self) -> Union[Session, SASession]:
        return Session(self.engine, expire_on_commit=False)


class SQLModelBase(SQLModel):
    __name__: str

    @classmethod
    def __tablename__(cls) -> str:
        # CamelCase to snake_case
        return camel_to_snake_case(cls.__name__)
