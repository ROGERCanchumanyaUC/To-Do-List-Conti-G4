from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class UsuarioSesion:
    """Representa el usuario autenticado (temporal, solo vista)."""

    id_usuario: int
    username: str


@dataclass
class TareaVista:
    """DTO de tarea para mostrar en UI (alineado a la BD)."""

    id_tarea: int
    id_usuario: int
    titulo: str
    descripcion: str | None
    completada: bool
    creada_en: datetime
    actualizada_en: datetime


class ControladorTareas(Protocol):
    """Contrato para conectar Vista → Lógica (se implementará luego)."""

    def listar(self, id_usuario: int) -> list[TareaVista]: ...
    def crear(
        self, id_usuario: int, titulo: str, descripcion: str | None
    ) -> TareaVista | None: ...
    def editar(
        self,
        id_usuario: int,
        id_tarea: int,
        titulo: str,
        descripcion: str | None,
    ) -> bool: ...
    def eliminar(self, id_usuario: int, id_tarea: int) -> bool: ...
    def marcar_completada(
        self, id_usuario: int, id_tarea: int, completada: bool
    ) -> bool: ...


class ControladorTareasEnMemoria:
    """Controlador temporal para la Vista (sin lógica real, sin BD)."""

    def __init__(self) -> None:
        self._auto_id = 1
        self._tareas: list[TareaVista] = []

    def listar(self, id_usuario: int) -> list[TareaVista]:
        return [t for t in self._tareas if t.id_usuario == id_usuario]

    def crear(
        self, id_usuario: int, titulo: str, descripcion: str | None
    ) -> TareaVista | None:
        titulo_limpio = (titulo or "").strip()
        if not titulo_limpio:
            return None

        # Simula restricción UNIQUE(id_usuario, titulo)
        for t in self._tareas:
            if t.id_usuario == id_usuario and t.titulo.lower() == titulo_limpio.lower():
                return None

        ahora = datetime.now()
        tarea = TareaVista(
            id_tarea=self._auto_id,
            id_usuario=id_usuario,
            titulo=titulo_limpio,
            descripcion=(descripcion or "").strip() if descripcion else None,
            completada=False,
            creada_en=ahora,
            actualizada_en=ahora,
        )
        self._auto_id += 1
        self._tareas.append(tarea)
        return tarea

    def editar(
        self,
        id_usuario: int,
        id_tarea: int,
        titulo: str,
        descripcion: str | None,
    ) -> bool:
        titulo_limpio = (titulo or "").strip()
        if not titulo_limpio:
            return False

        # Simula restricción UNIQUE(id_usuario, titulo)
        for t in self._tareas:
            if (
                t.id_usuario == id_usuario
                and t.id_tarea != id_tarea
                and t.titulo.lower() == titulo_limpio.lower()
            ):
                return False

        for t in self._tareas:
            if t.id_usuario == id_usuario and t.id_tarea == id_tarea:
                t.titulo = titulo_limpio
                t.descripcion = (descripcion or "").strip() if descripcion else None
                t.actualizada_en = datetime.now()
                return True
        return False

    def eliminar(self, id_usuario: int, id_tarea: int) -> bool:
        antes = len(self._tareas)
        self._tareas = [
            t for t in self._tareas if not (t.id_usuario == id_usuario and t.id_tarea == id_tarea)
        ]
        return len(self._tareas) != antes

    def marcar_completada(
        self, id_usuario: int, id_tarea: int, completada: bool
    ) -> bool:
        for t in self._tareas:
            if t.id_usuario == id_usuario and t.id_tarea == id_tarea:
                t.completada = bool(completada)
                t.actualizada_en = datetime.now()
                return True
        return False
