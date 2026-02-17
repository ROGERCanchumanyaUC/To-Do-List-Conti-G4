from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.vista.controlador_tareas_vista import TareaVista


@dataclass(frozen=True)
class DatosFormularioTarea:
    """Datos del formulario para crear/editar tarea."""

    titulo: str
    descripcion: str | None
    completada: bool


class FormularioTarea(QFrame):
    """Formulario lateral (Crear/Editar) para tareas."""

    guardar = pyqtSignal(object)  # DatosFormularioTarea
    cancelar = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("PanelFormulario")

        self._modo_edicion = False
        self._id_tarea: int | None = None

        self._lbl_titulo = QLabel("Formulario")
        self._lbl_titulo.setObjectName("TituloTarea")

        self._input_titulo = QLineEdit()
        self._input_titulo.setPlaceholderText("Título (obligatorio)")

        self._input_descripcion = QTextEdit()
        self._input_descripcion.setPlaceholderText("Descripción (opcional)")
        self._input_descripcion.setFixedHeight(120)

        self._chk_completada = QCheckBox("Marcar como completada")

        self._btn_guardar = QPushButton("Guardar")
        self._btn_guardar.setObjectName("BtnPrimario")
        self._btn_guardar.clicked.connect(self._emitir_guardar)

        self._btn_cancelar = QPushButton("Cancelar")
        self._btn_cancelar.setObjectName("BtnSecundario")
        self._btn_cancelar.clicked.connect(self.cancelar.emit)

        acciones = QHBoxLayout()
        acciones.addWidget(self._btn_cancelar)
        acciones.addWidget(self._btn_guardar)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        layout.addWidget(self._lbl_titulo)
        layout.addWidget(self._input_titulo)
        layout.addWidget(self._input_descripcion)
        layout.addWidget(self._chk_completada)
        layout.addStretch(1)
        layout.addLayout(acciones)

        self.modo_crear()

    @property
    def id_tarea(self) -> int | None:
        """Id de la tarea en edición (None si es creación)."""
        return self._id_tarea

    def modo_crear(self) -> None:
        """Configura el formulario para crear una tarea."""
        self._modo_edicion = False
        self._id_tarea = None
        self._lbl_titulo.setText("Crear tarea")
        self._btn_guardar.setText("Crear")
        self.limpiar()

    def modo_editar(self, tarea: TareaVista) -> None:
        """Configura el formulario para editar una tarea."""
        self._modo_edicion = True
        self._id_tarea = tarea.id_tarea
        self._lbl_titulo.setText(f"Editar tarea #{tarea.id_tarea}")
        self._btn_guardar.setText("Guardar cambios")

        self._input_titulo.setText(tarea.titulo)
        self._input_descripcion.setPlainText(tarea.descripcion or "")
        self._chk_completada.setChecked(bool(tarea.completada))

    def limpiar(self) -> None:
        """Limpia los campos del formulario."""
        self._input_titulo.clear()
        self._input_descripcion.clear()
        self._chk_completada.setChecked(False)

    def obtener_datos(self) -> DatosFormularioTarea:
        """Devuelve los datos actuales del formulario."""
        titulo = self._input_titulo.text()
        descripcion = self._input_descripcion.toPlainText().strip()
        return DatosFormularioTarea(
            titulo=titulo,
            descripcion=descripcion if descripcion else None,
            completada=self._chk_completada.isChecked(),
        )

    def _emitir_guardar(self) -> None:
        """Emite la señal guardar con los datos del formulario."""
        self.guardar.emit(self.obtener_datos())
