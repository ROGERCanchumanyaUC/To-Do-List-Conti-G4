# src/modelo/repositorio_tareas.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.modelo.bd_model import Tarea, Usuario

try:
    from src.modelo.conexion import SessionLocal  # type: ignore
except ImportError:  # pragma: no cover
    SessionLocal = None  # type: ignore


@dataclass(frozen=True)
class ResultadoOperacion:
    """Resultado estándar para operaciones CRUD."""
    ok: bool
    mensaje: str = ""


class RepositorioTareasSQLite:
    """
    Repositorio (SQLite + SQLAlchemy) para CRUD de tareas.

    - Maneja transacciones.
    - Controla errores de integridad (duplicados).
    - Evita que la capa lógica escriba SQL o maneje sesiones.
    """

    def __init__(self, session_factory: Optional[sessionmaker] = None) -> None:
        if session_factory is not None:
            self._session_factory = session_factory
            return

        if SessionLocal is None:
            raise RuntimeError(
                "No se encontró SessionLocal en src/modelo/conexion.py. "
                "Crea SessionLocal o inyecta un session_factory en el repositorio."
            )

        self._session_factory = SessionLocal

    def crear_tarea(
        self,
        id_usuario: int,
        titulo: str,
        descripcion: str | None = None,
    ) -> tuple[Tarea | None, str]:
        titulo = (titulo or "").strip()
        descripcion = (descripcion or "").strip() if descripcion is not None else None

        if not titulo:
            return None, "El título no puede estar vacío."

        try:
            with self._session_factory.begin() as session:
                if session.get(Usuario, id_usuario) is None:
                    return None, "El usuario no existe."

                tarea = Tarea(
                    id_usuario=id_usuario,
                    titulo=titulo,
                    descripcion=descripcion,
                    completada=False,
                )
                session.add(tarea)
                session.flush()         # genera id_tarea
                session.refresh(tarea)  # asegura valores actualizados

                # ✅ CLAVE: evita DetachedInstanceError tras commit/cierre de sesión
                session.expunge(tarea)

                return tarea, "Tarea creada correctamente."
        except IntegrityError:
            return None, "Ya existe una tarea con ese título para este usuario."

    def listar_tareas(self, id_usuario: int) -> list[Tarea]:
        with self._session_factory() as session:
            stmt = (
                select(Tarea)
                .where(Tarea.id_usuario == id_usuario)
                .order_by(Tarea.creada_en.desc())
            )
            return list(session.execute(stmt).scalars().all())

    def obtener_tarea(self, id_usuario: int, id_tarea: int) -> Tarea | None:
        with self._session_factory() as session:
            stmt = select(Tarea).where(
                Tarea.id_usuario == id_usuario,
                Tarea.id_tarea == id_tarea,
            )
            return session.execute(stmt).scalar_one_or_none()

    def editar_tarea(
        self,
        id_usuario: int,
        id_tarea: int,
        nuevo_titulo: str,
        nueva_descripcion: str | None = None,
    ) -> ResultadoOperacion:
        nuevo_titulo = (nuevo_titulo or "").strip()
        nueva_descripcion = (
            (nueva_descripcion or "").strip() if nueva_descripcion is not None else None
        )

        if not nuevo_titulo:
            return ResultadoOperacion(False, "El título no puede estar vacío.")

        try:
            with self._session_factory.begin() as session:
                tarea = self._get_tarea(session, id_usuario, id_tarea)
                if tarea is None:
                    return ResultadoOperacion(False, "La tarea no existe.")

                tarea.titulo = nuevo_titulo
                tarea.descripcion = nueva_descripcion
                return ResultadoOperacion(True, "Tarea actualizada correctamente.")
        except IntegrityError:
            return ResultadoOperacion(
                False,
                "Ya existe una tarea con ese título para este usuario.",
            )

    def eliminar_tarea(self, id_usuario: int, id_tarea: int) -> ResultadoOperacion:
        with self._session_factory.begin() as session:
            tarea = self._get_tarea(session, id_usuario, id_tarea)
            if tarea is None:
                return ResultadoOperacion(False, "La tarea no existe.")

            session.delete(tarea)
            return ResultadoOperacion(True, "Tarea eliminada correctamente.")

    def marcar_completada(
        self,
        id_usuario: int,
        id_tarea: int,
        completada: bool,
    ) -> ResultadoOperacion:
        with self._session_factory.begin() as session:
            tarea = self._get_tarea(session, id_usuario, id_tarea)
            if tarea is None:
                return ResultadoOperacion(False, "La tarea no existe.")

            tarea.completada = bool(completada)
            return ResultadoOperacion(True, "Estado actualizado correctamente.")

    @staticmethod
    def _get_tarea(session, id_usuario: int, id_tarea: int) -> Tarea | None:
        stmt = select(Tarea).where(
            Tarea.id_usuario == id_usuario,
            Tarea.id_tarea == id_tarea,
        )
        return session.execute(stmt).scalar_one_or_none()
