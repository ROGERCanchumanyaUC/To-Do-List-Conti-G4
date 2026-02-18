"""
Vista CRUD para registrar, editar y eliminar tareas.
Panel lateral izquierdo con formulario y panel derecho con tabla.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QLineEdit, QTextEdit,
    QCheckBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


class PantallaRegistrarTarea(QWidget):
    """Vista CRUD completa con formulario y tabla de tareas."""

    volver_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._configurar_ui()

    def _configurar_ui(self):
        """Configura la interfaz de la vista CRUD."""
        layout_externo = QVBoxLayout(self)
        layout_externo.setContentsMargins(0, 0, 0, 0)
        layout_externo.setSpacing(0)

        # ===== HEADER SUPERIOR =====
        header = QFrame()
        header.setStyleSheet(
            "QFrame { background-color: #ffffff; "
            "border-bottom: 1px solid rgba(0,0,0,0.08); }"
        )
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(28, 16, 28, 16)

        self.btn_volver = QPushButton("< Volver al Dashboard")
        self.btn_volver.setProperty("cssClass", "secondary")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setMinimumHeight(38)
        header_layout.addWidget(self.btn_volver)

        header_layout.addStretch()

        lbl_titulo = QLabel("Registrar Tarea")
        lbl_titulo.setProperty("cssClass", "titulo")
        header_layout.addWidget(lbl_titulo)

        header_layout.addStretch()

        # Espaciador para balancear el boton volver
        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(180)
        header_layout.addWidget(spacer_widget)

        layout_externo.addWidget(header)

        # ===== CONTENIDO PRINCIPAL =====
        contenido = QWidget()
        contenido_layout = QHBoxLayout(contenido)
        contenido_layout.setContentsMargins(28, 24, 28, 24)
        contenido_layout.setSpacing(24)

        # --- PANEL IZQUIERDO: FORMULARIO ---
        panel_form = QFrame()
        panel_form.setProperty("cssClass", "card")
        panel_form.setFixedWidth(380)
        form_layout = QVBoxLayout(panel_form)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(8)

        lbl_form_titulo = QLabel("Crear / Editar Tarea")
        lbl_form_titulo.setStyleSheet(
            "font-size: 18px; font-weight: 600; margin-bottom: 8px;"
        )
        form_layout.addWidget(lbl_form_titulo)

        lbl_form_desc = QLabel(
            "Completa los campos para registrar una nueva tarea"
        )
        lbl_form_desc.setProperty("cssClass", "subtitulo")
        lbl_form_desc.setWordWrap(True)
        form_layout.addWidget(lbl_form_desc)

        form_layout.addSpacing(16)

        # Campo: Titulo
        lbl_titulo_campo = QLabel("Titulo *")
        lbl_titulo_campo.setStyleSheet(
            "font-weight: 500; font-size: 13px;"
        )
        form_layout.addWidget(lbl_titulo_campo)

        self.txt_titulo = QLineEdit()
        self.txt_titulo.setPlaceholderText("Titulo de la tarea")
        self.txt_titulo.setMinimumHeight(42)
        form_layout.addWidget(self.txt_titulo)

        form_layout.addSpacing(10)

        # Campo: Descripcion
        lbl_descripcion = QLabel("Descripcion")
        lbl_descripcion.setStyleSheet(
            "font-weight: 500; font-size: 13px;"
        )
        form_layout.addWidget(lbl_descripcion)

        self.txt_descripcion = QTextEdit()
        self.txt_descripcion.setPlaceholderText(
            "Descripcion opcional de la tarea..."
        )
        self.txt_descripcion.setMinimumHeight(100)
        self.txt_descripcion.setMaximumHeight(140)
        form_layout.addWidget(self.txt_descripcion)

        form_layout.addSpacing(10)

        # Campo: Completada
        self.chk_completada = QCheckBox("Marcar como completada")
        form_layout.addWidget(self.chk_completada)

        form_layout.addSpacing(20)

        # Botones de accion
        botones_layout = QVBoxLayout()
        botones_layout.setSpacing(8)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setMinimumHeight(42)
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        botones_layout.addWidget(self.btn_guardar)

        fila_botones = QHBoxLayout()
        fila_botones.setSpacing(8)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setProperty("cssClass", "secondary")
        self.btn_actualizar.setMinimumHeight(42)
        self.btn_actualizar.setCursor(Qt.CursorShape.PointingHandCursor)
        fila_botones.addWidget(self.btn_actualizar)

        self.btn_eliminar = QPushButton("Eliminar")
        self.btn_eliminar.setProperty("cssClass", "danger")
        self.btn_eliminar.setMinimumHeight(42)
        self.btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        fila_botones.addWidget(self.btn_eliminar)

        botones_layout.addLayout(fila_botones)

        self.btn_limpiar = QPushButton("Limpiar Formulario")
        self.btn_limpiar.setProperty("cssClass", "secondary")
        self.btn_limpiar.setMinimumHeight(38)
        self.btn_limpiar.setCursor(Qt.CursorShape.PointingHandCursor)
        botones_layout.addWidget(self.btn_limpiar)

        form_layout.addLayout(botones_layout)
        form_layout.addStretch()

        contenido_layout.addWidget(panel_form)

        # --- PANEL DERECHO: TABLA ---
        panel_tabla = QFrame()
        panel_tabla.setProperty("cssClass", "card")
        tabla_layout = QVBoxLayout(panel_tabla)
        tabla_layout.setContentsMargins(24, 24, 24, 24)
        tabla_layout.setSpacing(12)

        lbl_tabla_titulo = QLabel("Listado de Tareas")
        lbl_tabla_titulo.setStyleSheet(
            "font-size: 18px; font-weight: 600;"
        )
        tabla_layout.addWidget(lbl_tabla_titulo)

        lbl_tabla_desc = QLabel(
            "Selecciona una tarea para editarla o eliminarla"
        )
        lbl_tabla_desc.setProperty("cssClass", "subtitulo")
        tabla_layout.addWidget(lbl_tabla_desc)

        tabla_layout.addSpacing(8)

        # Tabla de tareas
        self.tabla_tareas = QTableWidget()
        self.tabla_tareas.setColumnCount(6)
        self.tabla_tareas.setHorizontalHeaderLabels([
            "ID", "Titulo", "Descripcion",
            "Completada", "Creada en", "Actualizada en"
        ])
        self.tabla_tareas.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tabla_tareas.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabla_tareas.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tabla_tareas.setAlternatingRowColors(True)
        self.tabla_tareas.setStyleSheet(
            "QTableWidget { alternate-background-color: #fafafa; }"
        )
        self.tabla_tareas.verticalHeader().setVisible(False)

        # Ajustar columnas
        header_tabla = self.tabla_tareas.horizontalHeader()
        header_tabla.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        header_tabla.setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        header_tabla.setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        header_tabla.setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        header_tabla.setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents
        )
        header_tabla.setSectionResizeMode(
            5, QHeaderView.ResizeMode.ResizeToContents
        )

        tabla_layout.addWidget(self.tabla_tareas)

        # Placeholder cuando no hay tareas
        self.lbl_tabla_vacia = QLabel(
            "No hay tareas registradas. "
            "Usa el formulario para crear una."
        )
        self.lbl_tabla_vacia.setProperty("cssClass", "placeholder")
        self.lbl_tabla_vacia.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tabla_layout.addWidget(self.lbl_tabla_vacia)

        contenido_layout.addWidget(panel_tabla, 1)

        layout_externo.addWidget(contenido, 1)

        # ===== CONEXIONES =====
        self.btn_volver.clicked.connect(self.volver_clicked.emit)

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.txt_titulo.clear()
        self.txt_descripcion.clear()
        self.chk_completada.setChecked(False)
        self.tabla_tareas.clearSelection()

    def obtener_datos_formulario(self) -> dict:
        """Retorna los datos actuales del formulario como diccionario."""
        return {
            "titulo": self.txt_titulo.text().strip(),
            "descripcion": self.txt_descripcion.toPlainText().strip(),
            "completada": self.chk_completada.isChecked(),
        }

    def cargar_datos_formulario(self, datos: dict):
        """Carga datos en el formulario desde un diccionario."""
        self.txt_titulo.setText(datos.get("titulo", ""))
        self.txt_descripcion.setPlainText(
            datos.get("descripcion", "")
        )
        self.chk_completada.setChecked(
            datos.get("completada", False)
        )
