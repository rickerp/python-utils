import uuid

from sqlalchemy import Column as SAColumn
from sqlalchemy import ForeignKey as SAForeignKey
from sqlalchemy import Integer, TypeDecorator, create_engine, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session, sessionmaker

from utils.string import camel_to_snake_case

from .base import Database


class SQLAlchemyDatabase(Database):
    def __init__(self, user: str, password: str, host: str, port: str, name: str):
        super().__init__(user, password, host, port, name)
        self.engine = create_engine(self.database_uri, pool_pre_ping=True)
        self.sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def session(self) -> Session:
        return self.sessionmaker()


class SQLAlchemyBase:
    __name__: str

    def __init__(self, *args, **kwargs):
        # This is just for an IDE bug which it doesn't detect sqlalchemy declarative decorator functions
        super().__init__(*args, **kwargs)

    @declared_attr
    def __tablename__(cls) -> str:
        # CamelCase to snake_case
        return camel_to_snake_case(cls.__name__)

    def dict(self):
        """Returns a dictionary with all the model fields (excluding sqlalchemy relationships and metadata)"""
        return {k: v for k, v in self.__dict__.items() if k not in {'_sa_instance_state'}}


class IntEnum(TypeDecorator):
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)

    def __repr__(self):
        return 'sa.Integer()'


# Aliases

def Column(*args, nullable: bool = False, **kwargs):
    return SAColumn(*args, **kwargs, nullable=nullable)


def UUIDColumn(*args, **kwargs):  # pylint: disable=invalid-name
    return Column(
        UUID(as_uuid=True),
        *args,
        **kwargs,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()")
    )


def ForeignKey(*args, ondelete="CASCADE", **kwargs):
    return SAForeignKey(*args, **kwargs, ondelete=ondelete)
