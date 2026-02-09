# src/modelo/conexion.py
from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# ---------------------------------------------------------------------
# Configuración de base de datos (SQLite)
# Requisito: la BD debe persistir en el archivo "DB.sqlite" en la raíz.
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_FILENAME = "DB.sqlite"
DB_PATH = PROJECT_ROOT / DB_FILENAME
DATABASE_URL = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    """Base declarativa para los modelos ORM."""
    pass


def get_engine(*, echo: bool = False):
    """
    Crea el engine de SQLAlchemy para SQLite.

    - Activa PRAGMA foreign_keys=ON (obligatorio para que funcionen FKs en SQLite).
    - Configura WAL y synchronous=NORMAL como ajustes recomendados.
    """
    engine = create_engine(DATABASE_URL, echo=echo, future=True)

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

    return engine


ENGINE = get_engine(echo=False)

SessionLocal = sessionmaker(
    bind=ENGINE,
    autoflush=False,
    autocommit=False,
    future=True,
)


def init_db(*, echo: bool = False) -> None:
    """
    Crea/verifica las tablas en DB.sqlite.

    Importa los modelos dentro de la función para registrar las tablas
    en Base.metadata sin provocar imports circulares.
    """
    engine = get_engine(echo=echo)

    # Import requerido para que SQLAlchemy registre los modelos.
    from src.modelo.bd_model import Tarea, Usuario  # noqa: F401

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db(echo=True)
    print(f"✅ Base de datos creada/verificada en: {DB_PATH}")
