"""
Controlador de UI / mediador para la vista de tareas.
Mantiene una lista mock en memoria y conecta senales de los widgets.
NO usa SQLAlchemy ni accede a base de datos.
"""

from datetime import datetime
from PyQt6.QtWidgets import QMessageBox


class ControladorTareasVista:
    """Mediador entre las vistas del dashboard y registrar tarea."""

    def __init__(self, vista_dashboard, vista_registrar_tarea):
        self.dashboard = vista_dashboard
        self.registrar = vista_registrar_tarea
        self._tareas_mock: list[dict] = []
        self._id_siguiente: int = 1

        self._conectar_senales()
        self._refrescar_dashboard()

    def _conectar_senales(self):
        # Registrar tarea: guardar
        self.registrar.guardar_clicked.connect(self._al_guardar)

        # Dashboard: completar, editar, eliminar
        self.dashboard.completar_tarea_clicked.connect(self._completar_tarea)
        self.dashboard.editar_tarea_clicked.connect(self._editar_tarea)
        self.dashboard.eliminar_tarea_clicked.connect(self._eliminar_tarea)

        # Dashboard: buscar
        self.dashboard.buscar_clicked.connect(self._buscar_tareas)

    def _al_guardar(self, datos: dict):
        """Guardar nueva tarea o actualizar existente."""
        if not datos.get("titulo"):
            QMessageBox.warning(
                self.registrar,
                "Campo requerido",
                "El titulo de la tarea es obligatorio.",
            )
            return

        modo = datos.get("modo", "crear")

        if modo == "editar" and datos.get("id_tarea") is not None:
            for tarea in self._tareas_mock:
                if tarea["id_tarea"] == datos["id_tarea"]:
                    tarea["titulo"] = datos["titulo"]
                    tarea["descripcion"] = datos["descripcion"]
                    tarea["actualizada_en"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    break
        else:
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
            tarea = {
                "id_tarea": self._id_siguiente,
                "titulo": datos["titulo"],
                "descripcion": datos["descripcion"],
                "completada": False,
                "creada_en": ahora,
                "actualizada_en": ahora,
            }
            self._tareas_mock.append(tarea)
            self._id_siguiente += 1

        self.registrar.limpiar_formulario()
        self._refrescar_dashboard()

        # Volver al dashboard
        self.registrar.volver_clicked.emit()

    def _completar_tarea(self, id_tarea: int):
        """Marca una tarea como completada."""
        for tarea in self._tareas_mock:
            if tarea["id_tarea"] == id_tarea:
                tarea["completada"] = True
                tarea["actualizada_en"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                )
                break
        self._refrescar_dashboard()

    def _editar_tarea(self, id_tarea: int):
        """Carga una tarea en el formulario de edicion."""
        for tarea in self._tareas_mock:
            if tarea["id_tarea"] == id_tarea:
                self.registrar.cargar_para_edicion(tarea)
                stack = self.registrar.parent()
                if stack:
                    stack.setCurrentWidget(self.registrar)
                break

    def _eliminar_tarea(self, id_tarea: int):
        """Elimina una tarea (desde Completadas)."""
        self._tareas_mock = [
            t for t in self._tareas_mock if t["id_tarea"] != id_tarea
        ]
        self._refrescar_dashboard()

    def _buscar_tareas(self, texto: str):
        """Filtra tareas por nombre y refresca el dashboard."""
        if not texto:
            self._refrescar_dashboard()
            return

        filtradas = [
            t for t in self._tareas_mock
            if texto.lower() in t["titulo"].lower()
        ]
        self._mostrar_tareas(filtradas)

    def _refrescar_dashboard(self):
        """Actualiza estadisticas y lista de tareas en el dashboard."""
        stats = self.obtener_estadisticas()
        self.dashboard.actualizar_estadisticas(
            total=stats["total"],
            pendientes=stats["pendientes"],
            completadas=stats["completadas"],
        )
        self._mostrar_tareas(self._tareas_mock)

    def _mostrar_tareas(self, tareas: list):
        """Muestra las tareas en el dashboard."""
        self.dashboard.mostrar_tareas(tareas)

    def obtener_estadisticas(self) -> dict:
        total = len(self._tareas_mock)
        completadas = sum(1 for t in self._tareas_mock if t["completada"])
        pendientes = total - completadas
        return {
            "total": total,
            "pendientes": pendientes,
            "completadas": completadas,
        }
