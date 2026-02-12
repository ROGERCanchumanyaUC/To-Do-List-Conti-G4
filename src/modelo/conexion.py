# src/modelo/conexion.py
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "DB.sqlite"
DATABASE_URL = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    """Base declarativa para modelos ORM."""


def _create_engine(*, echo: bool = False) -> Engine:
    """Crea el engine SQLite y aplica PRAGMAs por conexión."""
    engine = create_engine(DATABASE_URL, echo=echo, future=True)

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=DELETE")  # solo DB.sqlite
        cursor.execute("PRAGMA synchronous=FULL")
        cursor.close()

    return engine


ENGINE = _create_engine(echo=False)

SessionLocal = sessionmaker(
    bind=ENGINE,
    autoflush=False,
    autocommit=False,
    future=True,
    class_=Session,
)


def crear_db_sqlite() -> Path:
    """Asegura que DB.sqlite exista."""
    with ENGINE.connect():
        pass
    return DB_PATH


@contextmanager
def get_session() -> Iterator[Session]:
    """
    Provee una sesión SQLAlchemy y garantiza cierre.

    Usage:
        with get_session() as session:
            ...
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Crea/verifica tablas en DB.sqlite según los modelos ORM."""

    from src.modelo.bd_model import Tarea, Usuario  # noqa: F401

    Base.metadata.create_all(bind=ENGINE)
