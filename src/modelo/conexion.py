from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "DB.sqlite"
DATABASE_URL = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    """Base declarativa para modelos ORM."""


ENGINE = create_engine(DATABASE_URL, echo=False, future=True)


def crear_db_sqlite() -> Path:
    """
    Crea el archivo DB.sqlite si no existe.
    SQLite crea el archivo al abrir una conexión.
    """
    with ENGINE.connect():
        pass
    return DB_PATH


def init_db() -> None:
    """
    Crea/verifica tablas en DB.sqlite según los modelos ORM.
    """
    # Importa aquí para evitar imports circulares
    from src.modelo.bd_model import Tarea, Usuario  # noqa: F401

    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    crear_db_sqlite()
    init_db()
    print(f"✅ DB.sqlite y tablas creadas/verificadas en: {DB_PATH}")
