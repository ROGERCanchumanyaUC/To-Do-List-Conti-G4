from src.modelo.modelo import Database
from src.modelo.task import Task

class TaskManager:
    def __init__(self, repositorio: RepositorioTareasSQLite | None = None) -> None:
        self._repo = repositorio or RepositorioTareasSQLite()

    # HU02 - Crear tarea
    def crear_tarea(self, id_usuario: int, titulo: str, descripcion: str = ""):
        titulo = (titulo or "").strip()
        if not titulo:
            raise ValueError("El título no puede estar vacío.")
        tarea, _msg = self._repo.crear_tarea(id_usuario, titulo, descripcion)
        return tarea

    # HU05 - Eliminar tarea
    def eliminar_tarea(self, id_usuario: int, id_tarea: int) -> bool:
        resultado = self._repo.eliminar_tarea(id_usuario, id_tarea)
        return bool(resultado.ok)
                description=row['description'],
                completed=bool(row['completed']),
                created_at=row['created_at']
            )
        return None
