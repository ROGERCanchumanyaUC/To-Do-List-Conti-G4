"""
Punto de entrada del sistema.
Inicializa la base de datos.
"""

from src.modelo.modelo import engine, Base
from src.modelo.task import Task  # noqa: F401


def init_db():
    """Crea las tablas en la base de datos."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Base de datos creada correctamente.")
