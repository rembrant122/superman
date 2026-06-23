from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Self

from sqlalchemy import Integer, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    Mapped,
    Query,
    Session,
    declarative_base,
    mapped_column,
    sessionmaker,
)

from settings import DATABASE_URL

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 30},
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

class AutomatisationDataBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def sanitize_string(cls, value: str) -> str:
        return value.encode("utf-8", errors="replace").decode("utf-8")

    @classmethod
    def find_by(cls, session: Session, **kwargs: Any) -> Query:
        query = session.query(cls)

        for key, value in kwargs.items():
            column = getattr(cls, key)

            if isinstance(value, list):
                query = query.filter(column.in_(value))
            else:
                query = query.filter(column == value)

        return query

    @classmethod
    def find_by_id(cls, session: Session, my_id: int) -> Self | None:
        return session.get(cls, my_id)

    @classmethod
    def add_something(cls, session: Session, **kwargs: Any) -> Self:
        prepared_kwargs: dict[str, Any] = {}

        for key, value in kwargs.items():
            if isinstance(value, str):
                prepared_kwargs[key] = cls.sanitize_string(value)
            else:
                prepared_kwargs[key] = value

        instance = cls(**prepared_kwargs)
        session.add(instance)
        return instance

    def delete(self, session: Session) -> None:
        session.delete(self)

    # @classmethod
    # def update(cls, session: Session, instance: Self, **kwargs: Any) -> Self:
    #     if instance is None:
    #         raise ValueError("Instance cannot be None")
    #
    #     for key, value in kwargs.items():
    #         if hasattr(instance, key):
    #             if isinstance(value, str):
    #                 value = cls.sanitize_string(value)
    #             setattr(instance, key, value)
    #
    #     return instance
