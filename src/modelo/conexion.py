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
    """Crea el engine SQLite con pragmas recomendados.

    Nota:
        - SQLite no aplica Foreign Keys por defecto: se activa con PRAGMA foreign_keys=ON.
        - Para que solo exista DB.sqlite (sin -wal ni -shm), usamos journal_mode=DELETE.
        - synchronous=FULL es consistente con DELETE (más seguro, un poco más lento).
    """
    engine = create_engine(
        DATABASE_URL,
        echo=echo,
        future=True,
    )

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=DELETE")
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
    """Asegura que DB.sqlite exista.

    SQLite crea el archivo físico al abrir una conexión.
    """
    with ENGINE.connect():
        pass
    return DB_PATH


@contextmanager
def get_session() -> Iterator[Session]:
    """Entrega una sesión SQLAlchemy lista para usar.

    Yields:
        Session: Sesión conectada a la base de datos.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Crea/verifica tablas en DB.sqlite según los modelos ORM."""
    # Import interno para registrar metadata sin ciclos de importación
    from src.modelo.bd_model import Tarea, Usuario  # noqa: F401

    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    crear_db_sqlite()
    init_db()
    print(f"✅ DB.sqlite y tablas creadas/verificadas en: {DB_PATH}")
