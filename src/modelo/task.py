"""
Modelo Task para la gestión de tareas.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.modelo.modelo import Base


class Task(Base):
    """
    Representa una tarea en el sistema.

    Attributes:
        id (int): Identificador único.
        descripcion (str): Texto de la tarea.
        completada (bool): Estado de la tarea.
        created_at (datetime): Fecha de creación.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(255), nullable=False, unique=True)
    completada = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
