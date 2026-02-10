"""
Gestor de tareas: lógica de negocio (CRUD).
"""

from sqlalchemy.exc import IntegrityError
from src.modelo.modelo import SessionLocal
from src.modelo.task import Task


class TaskManager:
    """Clase encargada de la gestión de tareas."""

    def __init__(self):
        self.db = SessionLocal()

    # HU02 - Crear tarea
    def crear_tarea(self, descripcion: str) -> Task:
        """Crea una nueva tarea."""
        try:
            tarea = Task(descripcion=descripcion)
            self.db.add(tarea)
            self.db.commit()
            self.db.refresh(tarea)
            return tarea
        except IntegrityError:
            self.db.rollback()
            raise ValueError("La tarea ya existe.")

    # HU03 - Ver tareas
    def listar_tareas(self):
        """Obtiene la lista de tareas."""
        return self.db.query(Task).all()

    # HU04 - Editar tarea
    def editar_tarea(self, tarea_id: int, nueva_descripcion: str):
        """Edita la descripción de una tarea."""
        tarea = self.db.query(Task).filter(Task.id == tarea_id).first()
        if not tarea:
            raise ValueError("Tarea no encontrada.")

        tarea.descripcion = nueva_descripcion
        self.db.commit()
        return tarea

    # HU05 - Eliminar tarea
    def eliminar_tarea(self, tarea_id: int):
        """Elimina una tarea."""
        tarea = self.db.query(Task).filter(Task.id == tarea_id).first()
        if not tarea:
            raise ValueError("Tarea no encontrada.")

        self.db.delete(tarea)
        self.db.commit()

    # HU06 - Marcar completada
    def marcar_completada(self, tarea_id: int):
        """Marca una tarea como completada."""
        tarea = self.db.query(Task).filter(Task.id == tarea_id).first()
        if not tarea:
            raise ValueError("Tarea no encontrada.")

        tarea.completada = True
        self.db.commit()
        return tarea
