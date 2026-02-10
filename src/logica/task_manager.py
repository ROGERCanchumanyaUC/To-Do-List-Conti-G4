# src/logica/task_manager.py
from __future__ import annotations

from src.modelo.repositorio_tareas import RepositorioTareasSQLite


class TaskManager:
    """Reglas de negocio para tareas (HU02–HU06)."""

    def __init__(self, repositorio: RepositorioTareasSQLite | None = None) -> None:
        self._repo = repositorio or RepositorioTareasSQLite()

    def crear_tarea(self, id_usuario: int, titulo: str, descripcion: str = ""):
        titulo = (titulo or "").strip()
        if not titulo:
            raise ValueError("El título no puede estar vacío.")

        tarea, _msg = self._repo.crear_tarea(id_usuario, titulo, descripcion)
        # Duplicado -> None (válido para tu HU)
        return tarea

    def listar_tareas(self, id_usuario: int):
        return self._repo.listar_tareas(id_usuario)

    def editar_tarea(
        self,
        id_usuario: int,
        id_tarea: int,
        nuevo_titulo: str,
        nueva_descripcion: str = "",
    ) -> bool:
        resultado = self._repo.editar_tarea(
            id_usuario,
            id_tarea,
            nuevo_titulo,
            nueva_descripcion,
        )
        return bool(resultado.ok)

    def eliminar_tarea(self, id_usuario: int, id_tarea: int) -> bool:
        resultado = self._repo.eliminar_tarea(id_usuario, id_tarea)
        return bool(resultado.ok)

    def marcar_completada(
        self,
        id_usuario: int,
        id_tarea: int,
        completada: bool,
    ) -> bool:
        resultado = self._repo.marcar_completada(id_usuario, id_tarea, completada)
        return bool(resultado.ok)
