from src.modelo.conexion import SessionLocal
from src.modelo.bd_model import Tarea


class EditarTareaLogica:
    """Lógica para editar tareas (HU Editar Tarea)."""

    def editar_tarea(
        self,
        id_tarea: int,
        nuevo_titulo: str,
        nueva_descripcion: str | None = None
    ) -> bool:
        """
        Edita una tarea existente.

        Returns:
            bool: True si se editó correctamente.
        """

        # Validación básica
        if not nuevo_titulo or not nuevo_titulo.strip():
            return False

        session = SessionLocal()

        try:
            tarea = session.query(Tarea).filter_by(id_tarea=id_tarea).first()

            if tarea is None:
                return False

            tarea.titulo = nuevo_titulo.strip()
            tarea.descripcion = nueva_descripcion

            session.commit()
            return True

        except Exception:
            session.rollback()
            return False

        finally:
            session.close()
