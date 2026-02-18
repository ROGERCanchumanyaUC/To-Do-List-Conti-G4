"""
Controlador de UI / mediador para la vista CRUD de tareas.
Mantiene una lista mock en memoria y conecta senales de los widgets.
NO usa SQLAlchemy ni accede a base de datos.
"""

from datetime import datetime
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt


class ControladorTareasVista:
    """Mediador entre los widgets de la vista CRUD de tareas."""

    def __init__(self, vista_registrar_tarea):
        """
        Inicializa el controlador con referencia a la vista CRUD.

        Args:
            vista_registrar_tarea: Instancia de PantallaRegistrarTarea.
        """
        self.vista = vista_registrar_tarea
        self._tareas_mock: list[dict] = []
        self._id_siguiente: int = 1
        self._indice_seleccionado: int | None = None

        self._conectar_senales()
        self._actualizar_tabla()

    def _conectar_senales(self):
        """Conecta las senales de los botones y la tabla."""
        self.vista.btn_guardar.clicked.connect(self._guardar_tarea)
        self.vista.btn_actualizar.clicked.connect(
            self._actualizar_tarea_seleccionada
        )
        self.vista.btn_eliminar.clicked.connect(
            self._eliminar_tarea_seleccionada
        )
        self.vista.btn_limpiar.clicked.connect(self._limpiar)
        self.vista.tabla_tareas.itemSelectionChanged.connect(
            self._al_seleccionar_fila
        )

    def _guardar_tarea(self):
        """Crea una nueva tarea con los datos del formulario."""
        datos = self.vista.obtener_datos_formulario()

        if not datos["titulo"]:
            QMessageBox.warning(
                self.vista,
                "Campo requerido",
                "El titulo de la tarea es obligatorio.",
            )
            return

        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tarea = {
            "id_tarea": self._id_siguiente,
            "titulo": datos["titulo"],
            "descripcion": datos["descripcion"],
            "completada": datos["completada"],
            "creada_en": ahora,
            "actualizada_en": ahora,
        }

        self._tareas_mock.append(tarea)
        self._id_siguiente += 1
        self._limpiar()
        self._actualizar_tabla()

    def _actualizar_tarea_seleccionada(self):
        """Actualiza la tarea seleccionada con los datos del formulario."""
        if self._indice_seleccionado is None:
            QMessageBox.information(
                self.vista,
                "Seleccion requerida",
                "Selecciona una tarea de la tabla para actualizar.",
            )
            return

        datos = self.vista.obtener_datos_formulario()

        if not datos["titulo"]:
            QMessageBox.warning(
                self.vista,
                "Campo requerido",
                "El titulo de la tarea es obligatorio.",
            )
            return

        tarea = self._tareas_mock[self._indice_seleccionado]
        tarea["titulo"] = datos["titulo"]
        tarea["descripcion"] = datos["descripcion"]
        tarea["completada"] = datos["completada"]
        tarea["actualizada_en"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self._limpiar()
        self._actualizar_tabla()

    def _eliminar_tarea_seleccionada(self):
        """Elimina la tarea seleccionada de la lista mock."""
        if self._indice_seleccionado is None:
            QMessageBox.information(
                self.vista,
                "Seleccion requerida",
                "Selecciona una tarea de la tabla para eliminar.",
            )
            return

        respuesta = QMessageBox.question(
            self.vista,
            "Confirmar eliminacion",
            "Estas seguro de que deseas eliminar esta tarea?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if respuesta == QMessageBox.StandardButton.Yes:
            del self._tareas_mock[self._indice_seleccionado]
            self._limpiar()
            self._actualizar_tabla()

    def _limpiar(self):
        """Limpia el formulario y la seleccion."""
        self._indice_seleccionado = None
        self.vista.limpiar_formulario()

    def _al_seleccionar_fila(self):
        """Maneja la seleccion de una fila en la tabla."""
        filas_seleccionadas = (
            self.vista.tabla_tareas.selectionModel().selectedRows()
        )

        if not filas_seleccionadas:
            self._indice_seleccionado = None
            return

        fila = filas_seleccionadas[0].row()
        self._indice_seleccionado = fila
        tarea = self._tareas_mock[fila]

        self.vista.cargar_datos_formulario({
            "titulo": tarea["titulo"],
            "descripcion": tarea["descripcion"],
            "completada": tarea["completada"],
        })

    def _actualizar_tabla(self):
        """Reconstruye la tabla con los datos mock actuales."""
        tabla = self.vista.tabla_tareas
        tabla.setRowCount(0)

        hay_tareas = len(self._tareas_mock) > 0
        tabla.setVisible(hay_tareas)
        self.vista.lbl_tabla_vacia.setVisible(not hay_tareas)

        for fila, tarea in enumerate(self._tareas_mock):
            tabla.insertRow(fila)

            tabla.setItem(
                fila, 0,
                QTableWidgetItem(str(tarea["id_tarea"]))
            )
            tabla.setItem(
                fila, 1,
                QTableWidgetItem(tarea["titulo"])
            )
            tabla.setItem(
                fila, 2,
                QTableWidgetItem(tarea["descripcion"])
            )
            tabla.setItem(
                fila, 3,
                QTableWidgetItem(
                    "Si" if tarea["completada"] else "No"
                )
            )
            tabla.setItem(
                fila, 4,
                QTableWidgetItem(tarea["creada_en"])
            )
            tabla.setItem(
                fila, 5,
                QTableWidgetItem(tarea["actualizada_en"])
            )

            # Centrar ciertas columnas
            for col in (0, 3):
                item = tabla.item(fila, col)
                if item:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

    def obtener_estadisticas(self) -> dict:
        """Retorna estadisticas de las tareas mock."""
        total = len(self._tareas_mock)
        completadas = sum(
            1 for t in self._tareas_mock if t["completada"]
        )
        pendientes = total - completadas
        return {
            "total": total,
            "pendientes": pendientes,
            "completadas": completadas,
        }
