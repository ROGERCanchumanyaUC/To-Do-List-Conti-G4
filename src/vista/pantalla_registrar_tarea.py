# src/vista/pantalla_registrar_tarea.py
from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.vista.controlador_tareas_vista import ControladorTareasVista, SesionVista, TareaVista


class PantallaRegistrarTarea(QWidget):
    volver_al_dashboard = pyqtSignal()

    def __init__(
        self,
        *,
        sesion: SesionVista,
        controlador: ControladorTareasVista,
        task_id: str | None = None,
    ) -> None:
        super().__init__()
        self.setObjectName("DashboardRoot")

        self._sesion = sesion
        self._controlador = controlador
        self._task_id = task_id

        self._btn_volver = QPushButton("Volver")
        self._btn_guardar = QPushButton("Guardar")
        self._btn_cancelar = QPushButton("Cancelar")

        self._input_nombre = QLineEdit()
        self._combo_categoria = QComboBox()
        self._spin_tiempo = QSpinBox()
        self._combo_unidad = QComboBox()
        self._input_detalle = QTextEdit()

        self._lbl_titulo = QLabel("Registrar Tarea")

        self._construir_ui()
        self._conectar_eventos()
        self._cargar_si_edicion()

    def _construir_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        # Header simple dentro del área
        header = QFrame()
        header.setObjectName("PanelBlanco")
        h = QHBoxLayout(header)
        h.setContentsMargins(18, 14, 18, 14)

        self._lbl_titulo.setObjectName("TituloGrande")
        self._lbl_titulo.setStyleSheet("font-size: 22px;")

        lbl_user = QLabel(self._sesion.username)
        lbl_user.setObjectName("Subtitulo")

        self._btn_volver.setObjectName("BotonSecundario")

        h.addWidget(self._lbl_titulo)
        h.addStretch(1)
        h.addWidget(lbl_user)
        h.addSpacing(10)
        h.addWidget(self._btn_volver)

        root.addWidget(header)

        # Formulario
        form = QFrame()
        form.setObjectName("PanelBlanco")
        f = QVBoxLayout(form)
        f.setContentsMargins(18, 18, 18, 18)
        f.setSpacing(10)

        self._input_nombre.setPlaceholderText("Nombre de la tarea")

        self._combo_categoria.addItems(
            ["Selecciona una categoría", "no importante", "obligatorio", "pendiente"]
        )

        self._spin_tiempo.setMinimum(1)
        self._spin_tiempo.setMaximum(999)
        self._spin_tiempo.setValue(1)

        self._combo_unidad.addItems(["días", "semanas", "meses"])

        self._input_detalle.setPlaceholderText("Describe los detalles de esta tarea...")

        row_tiempo = QHBoxLayout()
        row_tiempo.addWidget(self._spin_tiempo)
        row_tiempo.addWidget(self._combo_unidad)

        row_acciones = QHBoxLayout()
        self._btn_guardar.setObjectName("BotonPrimario")
        self._btn_cancelar.setObjectName("BotonSecundario")
        row_acciones.addStretch(1)
        row_acciones.addWidget(self._btn_cancelar)
        row_acciones.addWidget(self._btn_guardar)

        f.addWidget(QLabel("Nombre"))
        f.addWidget(self._input_nombre)
        f.addWidget(QLabel("Categoría"))
        f.addWidget(self._combo_categoria)
        f.addWidget(QLabel("Tiempo estimado"))
        f.addLayout(row_tiempo)
        f.addWidget(QLabel("Detalle"))
        f.addWidget(self._input_detalle, 1)
        f.addLayout(row_acciones)

        root.addWidget(form, 1)

    def _conectar_eventos(self) -> None:
        self._btn_volver.clicked.connect(self.volver_al_dashboard.emit)
        self._btn_cancelar.clicked.connect(self._on_cancelar)
        self._btn_guardar.clicked.connect(self._on_guardar)

    def _cargar_si_edicion(self) -> None:
        if self._task_id is None:
            self._lbl_titulo.setText("Registrar Tarea")
            return

        tarea = self._buscar_tarea(self._task_id)
        if tarea is None:
            QMessageBox.warning(self, "Aviso", "La tarea no existe o fue eliminada.")
            self.volver_al_dashboard.emit()
            return

        self._lbl_titulo.setText("Editar Tarea")
        self._input_nombre.setText(tarea.name)

        idx = self._combo_categoria.findText(tarea.category)
        self._combo_categoria.setCurrentIndex(idx if idx >= 0 else 0)

        self._spin_tiempo.setValue(int(tarea.time_value))

        idx_u = self._combo_unidad.findText(tarea.time_unit)
        self._combo_unidad.setCurrentIndex(idx_u if idx_u >= 0 else 0)

        self._input_detalle.setPlainText(tarea.detail)

    def _buscar_tarea(self, task_id: str) -> TareaVista | None:
        for t in self._controlador.tareas:
            if t.id == task_id:
                return t
        return None

    def _on_cancelar(self) -> None:
        self.volver_al_dashboard.emit()

    def _on_guardar(self) -> None:
        nombre = (self._input_nombre.text() or "").strip()
        categoria = self._combo_categoria.currentText()
        tiempo = int(self._spin_tiempo.value())
        unidad = self._combo_unidad.currentText()
        detalle = (self._input_detalle.toPlainText() or "").strip()

        if not nombre:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return

        if categoria == "Selecciona una categoría":
            QMessageBox.warning(self, "Validación", "Selecciona una categoría válida.")
            return

        if tiempo <= 0:
            QMessageBox.warning(self, "Validación", "El tiempo debe ser mayor a 0.")
            return

        if not detalle:
            QMessageBox.warning(self, "Validación", "El detalle no puede estar vacío.")
            return

        if self._task_id is None:
            self._controlador.agregar_tarea(
                name=nombre,
                category=categoria,
                time_value=tiempo,
                time_unit=unidad,
                detail=detalle,
            )
        else:
            self._controlador.editar_tarea(
                self._task_id,
                name=nombre,
                category=categoria,
                time_value=tiempo,
                time_unit=unidad,
                detail=detalle,
            )

        self.volver_al_dashboard.emit()
