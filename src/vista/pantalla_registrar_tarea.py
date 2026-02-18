"""
Vista para registrar una nueva tarea - formulario simple sin tabla.
Solo titulo, descripcion, y botones Guardar/Cancelar.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QTextEdit,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor


class PantallaRegistrarTarea(QWidget):
    """Vista de formulario para registrar/editar una tarea."""

    volver_clicked = pyqtSignal()
    guardar_clicked = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._modo_edicion = False
        self._id_edicion = None
        self._configurar_ui()

    def _configurar_ui(self):
        layout_externo = QVBoxLayout(self)
        layout_externo.setContentsMargins(0, 0, 0, 0)
        layout_externo.setSpacing(0)

        # ===== HEADER =====
        header = QFrame()
        header.setProperty("cssClass", "header-bar")
        header.setFixedHeight(68)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(32, 0, 32, 0)

        self.btn_volver = QPushButton("\u2190  Volver")
        self.btn_volver.setProperty("cssClass", "ghost")
        self.btn_volver.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_volver.setMinimumHeight(38)
        header_layout.addWidget(self.btn_volver)

        header_layout.addStretch()

        self.lbl_titulo_header = QLabel("Registrar Tarea")
        self.lbl_titulo_header.setStyleSheet(
            "font-size: 18px; font-weight: 700; color: #ffffff;"
        )
        header_layout.addWidget(self.lbl_titulo_header)

        header_layout.addStretch()

        spacer = QWidget()
        spacer.setFixedWidth(100)
        header_layout.addWidget(spacer)

        layout_externo.addWidget(header)

        # ===== CONTENIDO CENTRADO =====
        contenido = QWidget()
        contenido.setStyleSheet(
            "background: qlineargradient("
            "x1:0, y1:0, x2:1, y2:1, stop:0 #dbeafe, stop:1 #ffffff);"
        )
        contenido_layout = QVBoxLayout(contenido)
        contenido_layout.setContentsMargins(0, 48, 0, 48)
        contenido_layout.setSpacing(0)

        contenido_layout.addStretch()
        h_center = QHBoxLayout()
        h_center.addStretch()

        # --- CARD FORMULARIO ---
        panel_form = QFrame()
        panel_form.setProperty("cssClass", "card")
        panel_form.setFixedWidth(520)
        panel_form.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )

        sombra_form = QGraphicsDropShadowEffect(panel_form)
        sombra_form.setBlurRadius(30)
        sombra_form.setOffset(0, 6)
        sombra_form.setColor(QColor(0, 0, 0, 18))
        panel_form.setGraphicsEffect(sombra_form)

        form_layout = QVBoxLayout(panel_form)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(0)

        self.lbl_form_titulo = QLabel("Nueva Tarea")
        self.lbl_form_titulo.setStyleSheet(
            "font-size: 22px; font-weight: 700; color: #1a1a2e;"
        )
        self.lbl_form_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.lbl_form_titulo)

        form_layout.addSpacing(6)

        self.lbl_form_desc = QLabel(
            "Completa los campos para registrar una nueva tarea"
        )
        self.lbl_form_desc.setProperty("cssClass", "subtitulo")
        self.lbl_form_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_form_desc.setWordWrap(True)
        form_layout.addWidget(self.lbl_form_desc)

        form_layout.addSpacing(32)

        # Campo: Titulo
        lbl_titulo_campo = QLabel("Titulo")
        lbl_titulo_campo.setProperty("cssClass", "campo-label")
        form_layout.addWidget(lbl_titulo_campo)

        form_layout.addSpacing(6)

        self.txt_titulo = QLineEdit()
        self.txt_titulo.setPlaceholderText("Titulo de la tarea")
        self.txt_titulo.setMinimumHeight(46)
        form_layout.addWidget(self.txt_titulo)

        form_layout.addSpacing(20)

        # Campo: Descripcion
        lbl_descripcion = QLabel("Descripcion")
        lbl_descripcion.setProperty("cssClass", "campo-label")
        form_layout.addWidget(lbl_descripcion)

        form_layout.addSpacing(6)

        self.txt_descripcion = QTextEdit()
        self.txt_descripcion.setPlaceholderText("Descripcion de la tarea...")
        self.txt_descripcion.setMinimumHeight(120)
        self.txt_descripcion.setMaximumHeight(160)
        form_layout.addWidget(self.txt_descripcion)

        form_layout.addSpacing(32)

        # Botones: Guardar y Cancelar
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(12)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setProperty("cssClass", "secondary")
        self.btn_cancelar.setMinimumHeight(46)
        self.btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        botones_layout.addWidget(self.btn_cancelar)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setProperty("cssClass", "guardar")  # <-- cambio mínimo
        self.btn_guardar.setMinimumHeight(46)
        self.btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        botones_layout.addWidget(self.btn_guardar)

        form_layout.addLayout(botones_layout)

        h_center.addWidget(panel_form)
        h_center.addStretch()

        contenido_layout.addLayout(h_center)
        contenido_layout.addStretch()

        layout_externo.addWidget(contenido, 1)

        # ===== CONEXIONES =====
        self.btn_volver.clicked.connect(self._al_cancelar)
        self.btn_cancelar.clicked.connect(self._al_cancelar)
        self.btn_guardar.clicked.connect(self._al_guardar)

    def _al_guardar(self):
        datos = self.obtener_datos_formulario()
        if self._modo_edicion and self._id_edicion is not None:
            datos["id_tarea"] = self._id_edicion
            datos["modo"] = "editar"
        else:
            datos["modo"] = "crear"
        self.guardar_clicked.emit(datos)

    def _al_cancelar(self):
        self.limpiar_formulario()
        self.volver_clicked.emit()

    def limpiar_formulario(self):
        self.txt_titulo.clear()
        self.txt_descripcion.clear()
        self._modo_edicion = False
        self._id_edicion = None
        self.lbl_titulo_header.setText("Registrar Tarea")
        self.lbl_form_titulo.setText("Nueva Tarea")
        self.lbl_form_desc.setText(
            "Completa los campos para registrar una nueva tarea"
        )

    def cargar_para_edicion(self, datos: dict):
        """Carga datos de una tarea existente para editar."""
        self._modo_edicion = True
        self._id_edicion = datos.get("id_tarea")
        self.txt_titulo.setText(datos.get("titulo", ""))
        self.txt_descripcion.setPlainText(datos.get("descripcion", ""))
        self.lbl_titulo_header.setText("Editar Tarea")
        self.lbl_form_titulo.setText("Editar Tarea")
        self.lbl_form_desc.setText("Modifica los campos y guarda los cambios")

    def obtener_datos_formulario(self) -> dict:
        return {
            "titulo": self.txt_titulo.text().strip(),
            "descripcion": self.txt_descripcion.toPlainText().strip(),
        }
