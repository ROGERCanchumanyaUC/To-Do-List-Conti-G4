# src/logica/task_manager.py
from __future__ import annotations
from datetime import datetime

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

    def listar_tareas_por_estado(self, id_usuario: int, completada: bool):
        """
        Lista tareas filtrando por estado (pendiente/completada).
        - completada=False -> pendientes
        - completada=True  -> completadas
        """
        tareas = self.listar_tareas(id_usuario)
        return [t for t in tareas if bool(getattr(t, "completada", False)) == bool(completada)]
    def listar_tareas_ordenadas(self, id_usuario: int, orden: str = "fecha"):
        """
        HU10: Lista tareas del usuario ordenadas.
        orden:
        - "fecha"  -> más recientes primero
        - "nombre" -> alfabético por título
        """
        tareas = self.listar_tareas(id_usuario)
        orden = (orden or "fecha").strip().lower()

        if orden == "nombre":
            return sorted(
                tareas,
                key=lambda t: (getattr(t, "titulo", "") or "").lower(),
            )

        # Por fecha (más reciente primero)
        def key_fecha(t):
            v = getattr(t, "creada_en", None)
            return v if v is not None else datetime.min

        return sorted(tareas, key=key_fecha, reverse=True)