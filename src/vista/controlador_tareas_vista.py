"""
Controlador de UI / mediador para la vista de tareas.
Conecta señales de widgets con la capa lógica (TaskManager).
"""

from __future__ import annotations

from datetime import datetime
from PyQt6.QtWidgets import QMessageBox

from src.logica.task_manager import TaskManager


class ControladorTareasVista:
    """Mediador entre dashboard/registrar y la lógica de tareas."""

    def __init__(
        self,
        vista_dashboard,
        vista_registrar_tarea,
        task_manager: TaskManager | None = None,
    ):
        self.dashboard = vista_dashboard
        self.registrar = vista_registrar_tarea
        self._task_manager = task_manager or TaskManager()

        self._id_usuario: int | None = None

        self._conectar_senales()
        self._refrescar_dashboard()

    def set_usuario(self, id_usuario: int | None) -> None:
        """Setea el usuario actual (para filtrar tareas por usuario)."""
        self._id_usuario = id_usuario
        self._refrescar_dashboard()

    def _conectar_senales(self):
        self.registrar.guardar_clicked.connect(self._al_guardar)

        self.dashboard.completar_tarea_clicked.connect(self._completar_tarea)
        self.dashboard.editar_tarea_clicked.connect(self._editar_tarea)
        self.dashboard.eliminar_tarea_clicked.connect(self._eliminar_tarea)

        self.dashboard.buscar_clicked.connect(self._buscar_tareas)

    def _al_guardar(self, datos: dict):
        """Crear o editar tarea en BD."""
        if self._id_usuario is None:
            QMessageBox.warning(
                self.registrar,
                "Sesión no válida",
                "No hay un usuario autenticado.",
            )
            return

        titulo = (datos.get("titulo") or "").strip()
        descripcion = (datos.get("descripcion") or "").strip()

        if not titulo:
            QMessageBox.warning(
                self.registrar,
                "Campo requerido",
                "El titulo de la tarea es obligatorio.",
            )
            return

        modo = datos.get("modo", "crear")

        if modo == "editar" and datos.get("id_tarea") is not None:
            ok = self._task_manager.editar_tarea(
                self._id_usuario,
                int(datos["id_tarea"]),
                titulo,
                descripcion,
            )
            if not ok:
                QMessageBox.warning(
                    self.registrar,
                    "No se pudo actualizar",
                    "No se pudo actualizar la tarea. "
                    "Verifica que no exista otra con el mismo título.",
                )
                return
        else:
            tarea = self._task_manager.crear_tarea(
                self._id_usuario,
                titulo,
                descripcion,
            )
            if tarea is None:
                QMessageBox.warning(
                    self.registrar,
                    "No se pudo crear",
                    "No se pudo crear la tarea. "
                    "Puede que ya exista una con ese título.",
                )
                return

        self.registrar.limpiar_formulario()
        self._refrescar_dashboard()
        self.registrar.volver_clicked.emit()

    def _completar_tarea(self, id_tarea: int):
        """Marca como completada."""
        if self._id_usuario is None:
            return

        self._task_manager.marcar_completada(
            self._id_usuario,
            int(id_tarea),
            True,
        )
        self._refrescar_dashboard()
        
    def _editar_tarea(self, id_tarea: int):
        """Carga una tarea en el formulario de edición."""
        if self._id_usuario is None:
            return

        tareas = self._obtener_tareas_dict()
        for tarea in tareas:
            if tarea["id_tarea"] == int(id_tarea):
                self.registrar.cargar_para_edicion(tarea)
                stack = self.registrar.parent()
                if stack:
                    stack.setCurrentWidget(self.registrar)
                break

    def _buscar_tareas(self, texto: str):
        """Filtra tareas por título y refresca el dashboard."""
        if self._id_usuario is None:
            self._mostrar_tareas([])
            return

        texto = (texto or "").strip()
        tareas = self._obtener_tareas_dict()

        if not texto:
            self._refrescar_dashboard()
            return

        filtradas = [
            t for t in tareas if texto.lower() in t["titulo"].lower()
        ]
        self._mostrar_tareas(filtradas)

    def _refrescar_dashboard(self):
        """Actualiza stats y lista de tareas."""
        tareas = self._obtener_tareas_dict()

        total = len(tareas)
        completadas = sum(1 for t in tareas if t["completada"])
        pendientes = total - completadas

        self.dashboard.actualizar_estadisticas(
            total=total,
            pendientes=pendientes,
            completadas=completadas,
        )
        self._mostrar_tareas(tareas)

    def _mostrar_tareas(self, tareas: list[dict]):
        self.dashboard.mostrar_tareas(tareas)

    def _obtener_tareas_dict(self) -> list[dict]:
        """Lee tareas desde la lógica y las convierte al formato que usa la vista."""
        if self._id_usuario is None:
            return []

        tareas = self._task_manager.listar_tareas(self._id_usuario)
        return [self._tarea_a_dict(t) for t in tareas]
    
    def _eliminar_tarea(self, id_tarea: int):
        """Elimina tarea (desde completadas) con confirmación."""
        if self._id_usuario is None:
            return

        # (Opcional) Obtener título para mostrar en el mensaje
        titulo = ""
        tareas = self._obtener_tareas_dict()
        for t in tareas:
            if t["id_tarea"] == int(id_tarea):
                titulo = t.get("titulo", "")
                break

        texto = (
            f"¿Seguro que deseas eliminar la tarea:\n\n“{titulo}”?\n\n"
            "Esta acción no se puede deshacer."
            if titulo
            else "¿Seguro que deseas eliminar esta tarea?\n\nEsta acción no se puede deshacer."
        )

        respuesta = QMessageBox.question(
            self.dashboard,                 # o self.registrar, cualquiera como parent
            "Confirmar eliminación",
            texto,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,  # por defecto NO
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return  # Cancelado por el usuario

        self._task_manager.eliminar_tarea(self._id_usuario, int(id_tarea))
        self._refrescar_dashboard()

    @staticmethod
    def _tarea_a_dict(tarea) -> dict:
        creada = ControladorTareasVista._fmt_dt(getattr(tarea, "creada_en", None))
        actualizada = ControladorTareasVista._fmt_dt(
            getattr(tarea, "actualizada_en", None)
        )

        return {
            "id_tarea": int(getattr(tarea, "id_tarea")),
            "titulo": str(getattr(tarea, "titulo") or ""),
            "descripcion": str(getattr(tarea, "descripcion") or ""),
            "completada": bool(getattr(tarea, "completada")),
            "creada_en": creada,
            "actualizada_en": actualizada,
        }

    @staticmethod
    def _fmt_dt(valor) -> str:
        if valor is None:
            return ""
        if isinstance(valor, datetime):
            return valor.strftime("%Y-%m-%d %H:%M")
        return str(valor)
