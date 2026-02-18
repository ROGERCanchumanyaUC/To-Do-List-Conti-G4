"""
Vista para registrar/editar una tarea.
Formulario centrado: titulo, descripcion, y botones Guardar/Cancelar.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QLineEdit,
    QTextEdit,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor

from src.vista.animaciones import BotonAnimado


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
        header.setFixedHeight(72)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(36, 0, 36, 0)

        self.btn_volver = BotonAnimado(
            "\u2190  Volver",
            color_sombra="#ffffff",
            intensidad_sombra=30,
            blur_reposo=0,
            blur_hover=12.0,
        )
        self.btn_volver.setProperty("cssClass", "btn-volver")
        self.btn_volver.setMinimumHeight(40)
        header_layout.addWidget(self.btn_volver)

        header_layout.addStretch()

        self.lbl_titulo_header = QLabel("Registrar Tarea")
        self.lbl_titulo_header.setStyleSheet(
            "font-size: 20px; font-weight: 800; color: #ffffff;"
            "letter-spacing: -0.3px;"
        )
        header_layout.addWidget(self.lbl_titulo_header)

        header_layout.addStretch()

        spacer = QWidget()
        spacer.setFixedWidth(110)
        header_layout.addWidget(spacer)

        layout_externo.addWidget(header)

        # ===== CONTENIDO CENTRADO =====
        contenido = QWidget()
        contenido.setStyleSheet("background-color: #e8ecf1;")
        contenido_layout = QVBoxLayout(contenido)
        contenido_layout.setContentsMargins(0, 52, 0, 52)
        contenido_layout.setSpacing(0)

        contenido_layout.addStretch()
        h_center = QHBoxLayout()
        h_center.addStretch()

        # --- CARD FORMULARIO ---
        panel_form = QFrame()
        panel_form.setProperty("cssClass", "card")
        panel_form.setFixedWidth(540)
        panel_form.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )

        sombra_form = QGraphicsDropShadowEffect(panel_form)
        sombra_form.setBlurRadius(40)
        sombra_form.setOffset(0, 8)
        sombra_form.setColor(QColor(79, 70, 229, 22))
        panel_form.setGraphicsEffect(sombra_form)

        form_layout = QVBoxLayout(panel_form)
        form_layout.setContentsMargins(44, 44, 44, 44)
        form_layout.setSpacing(0)

        # Icono del formulario
        icono_container = QHBoxLayout()
        icono_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_icono = QLabel()
        lbl_icono.setFixedSize(48, 48)
        lbl_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icono.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1,"
            "stop:0 #7c3aed, stop:1 #4f46e5);"
            "border-radius: 24px;"
            "color: #ffffff;"
            "font-size: 20px;"
            "font-weight: 700;"
        )
        lbl_icono.setText("\u270E")
        icono_container.addWidget(lbl_icono)
        form_layout.addLayout(icono_container)

        form_layout.addSpacing(18)

        self.lbl_form_titulo = QLabel("Nueva Tarea")
        self.lbl_form_titulo.setStyleSheet(
            "font-size: 24px; font-weight: 800; color: #1a1a2e;"
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

        form_layout.addSpacing(36)

        # Campo: Titulo
        lbl_titulo_campo = QLabel("Titulo")
        lbl_titulo_campo.setProperty("cssClass", "campo-label")
        form_layout.addWidget(lbl_titulo_campo)

        form_layout.addSpacing(6)

        self.txt_titulo = QLineEdit()
        self.txt_titulo.setPlaceholderText("Titulo de la tarea")
        self.txt_titulo.setMinimumHeight(48)
        form_layout.addWidget(self.txt_titulo)

        form_layout.addSpacing(22)

        # Campo: Descripcion
        lbl_descripcion = QLabel("Descripcion")
        lbl_descripcion.setProperty("cssClass", "campo-label")
        form_layout.addWidget(lbl_descripcion)

        form_layout.addSpacing(6)

        self.txt_descripcion = QTextEdit()
        self.txt_descripcion.setPlaceholderText("Descripcion de la tarea...")
        self.txt_descripcion.setMinimumHeight(130)
        self.txt_descripcion.setMaximumHeight(170)
        form_layout.addWidget(self.txt_descripcion)

        form_layout.addSpacing(36)

        # Botones: Cancelar y Guardar (animados, colores distintos)
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(14)

        self.btn_cancelar = BotonAnimado(
            "Cancelar",
            color_sombra="#4b5563",
            intensidad_sombra=50,
            blur_reposo=2.0,
            blur_hover=16.0,
        )
        self.btn_cancelar.setProperty("cssClass", "btn-cancelar")
        self.btn_cancelar.setMinimumHeight(48)
        self.btn_cancelar.setStyleSheet(
            "QPushButton { background-color: #d1d5db; color: #1a1a2e;"
            " border: none; border-radius: 12px; padding: 11px 36px;"
            " font-size: 14px; font-weight: 700; }"
            "QPushButton:hover { background-color: #b0b5bd; }"
            "QPushButton:pressed { background-color: #9ca3af; }"
        )
        botones_layout.addWidget(self.btn_cancelar)

        self.btn_guardar = BotonAnimado(
            "Guardar",
            color_sombra="#7c3aed",
            intensidad_sombra=60,
            blur_reposo=2.0,
            blur_hover=18.0,
        )
        self.btn_guardar.setProperty("cssClass", "btn-guardar")
        self.btn_guardar.setMinimumHeight(48)
        self.btn_guardar.setStyleSheet(
            "QPushButton { background-color: #7c3aed; color: #1a1a2e;"
            " border: none; border-radius: 12px; padding: 11px 36px;"
            " font-size: 14px; font-weight: 700; }"
            "QPushButton:hover { background-color: #6d28d9; }"
            "QPushButton:pressed { background-color: #5b21b6; }"
        )
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
