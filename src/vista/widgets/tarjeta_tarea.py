from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.vista.controlador_tareas_vista import TareaVista


class TarjetaTarea(QFrame):
    """Tarjeta visual para mostrar una tarea en el listado."""

    editar = pyqtSignal(int)  # id_tarea
    eliminar = pyqtSignal(int)  # id_tarea
    alternar_completada = pyqtSignal(int, bool)  # id_tarea, completada

    def __init__(self, tarea: TareaVista, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("TarjetaTarea")
        self._tarea = tarea

        titulo = QLabel(tarea.titulo)
        titulo.setObjectName("TituloTarea")

        meta_txt = self._formatear_meta(tarea)
        meta = QLabel(meta_txt)
        meta.setObjectName("MetaTarea")
        meta.setWordWrap(True)

        btn_editar = QPushButton("Editar")
        btn_editar.setObjectName("BtnAccion")
        btn_editar.clicked.connect(lambda: self.editar.emit(self._tarea.id_tarea))

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("BtnAccion")
        btn_eliminar.clicked.connect(lambda: self.eliminar.emit(self._tarea.id_tarea))

        btn_toggle = QPushButton("Completar" if not tarea.completada else "Reabrir")
        btn_toggle.setObjectName("BtnAccion")
        btn_toggle.clicked.connect(self._toggle_completada)

        acciones = QHBoxLayout()
        acciones.setSpacing(8)
        acciones.addWidget(btn_toggle)
        acciones.addStretch(1)
        acciones.addWidget(btn_editar)
        acciones.addWidget(btn_eliminar)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)
        layout.addWidget(titulo)
        if tarea.descripcion:
            desc = QLabel(tarea.descripcion)
            desc.setObjectName("MetaTarea")
            desc.setWordWrap(True)
            layout.addWidget(desc)
        layout.addWidget(meta)
        layout.addLayout(acciones)

    @staticmethod
    def _formatear_meta(tarea: TareaVista) -> str:
        estado = "Completada ✅" if tarea.completada else "Pendiente ⏳"
        return (
            f"ID: {tarea.id_tarea}  •  {estado}\n"
            f"Creada: {tarea.creada_en:%Y-%m-%d %H:%M}  •  "
            f"Actualizada: {tarea.actualizada_en:%Y-%m-%d %H:%M}"
        )

    def _toggle_completada(self) -> None:
        nueva = not bool(self._tarea.completada)
        self.alternar_completada.emit(self._tarea.id_tarea, nueva)
