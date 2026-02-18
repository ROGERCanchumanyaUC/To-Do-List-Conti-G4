"""
Pantalla de inicio de sesion - diseño profesional con card centrado.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QSizePolicy,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor


class PantallaLogin(QWidget):
    """Pantalla de login a pantalla completa con card centrado."""

    sesion_iniciada = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("cssClass", "login-fondo")
        self._configurar_ui()

    def _configurar_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        layout_horizontal = QHBoxLayout()
        layout_horizontal.setContentsMargins(0, 0, 0, 0)

        layout_principal.addStretch(1)
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addStretch(1)

        layout_horizontal.addStretch(1)

        self.card = QFrame()
        self.card.setProperty("cssClass", "login-card")
        self.card.setFixedWidth(420)
        self.card.setMaximumHeight(540)
        self.card.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )

        sombra = QGraphicsDropShadowEffect(self.card)
        sombra.setBlurRadius(40)
        sombra.setOffset(0, 8)
        sombra.setColor(QColor(0, 0, 0, 25))
        self.card.setGraphicsEffect(sombra)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(44, 48, 44, 44)
        card_layout.setSpacing(0)

        icono_container = QHBoxLayout()
        icono_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_icono = QLabel()
        lbl_icono.setFixedSize(52, 52)
        lbl_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icono.setStyleSheet(
            "background-color: #1a1a2e;"
            "border-radius: 26px;"
            "color: #ffffff;"
            "font-size: 22px;"
            "font-weight: 700;"
        )
        lbl_icono.setText("\u2713")
        icono_container.addWidget(lbl_icono)
        card_layout.addLayout(icono_container)

        card_layout.addSpacing(20)

        lbl_titulo = QLabel("Bienvenido de vuelta")
        lbl_titulo.setProperty("cssClass", "titulo")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_titulo)

        card_layout.addSpacing(6)

        lbl_subtitulo = QLabel("Ingresa tus credenciales para continuar")
        lbl_subtitulo.setProperty("cssClass", "subtitulo")
        lbl_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_subtitulo)

        card_layout.addSpacing(32)

        lbl_usuario = QLabel("Usuario")
        lbl_usuario.setProperty("cssClass", "campo-label")
        card_layout.addWidget(lbl_usuario)

        card_layout.addSpacing(6)

        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Ingresa tu usuario")
        self.txt_usuario.setMinimumHeight(44)
        card_layout.addWidget(self.txt_usuario)

        card_layout.addSpacing(18)

        lbl_contrasena = QLabel("Contrasena")
        lbl_contrasena.setProperty("cssClass", "campo-label")
        card_layout.addWidget(lbl_contrasena)

        card_layout.addSpacing(6)

        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setPlaceholderText("Ingresa tu contrasena")
        self.txt_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_contrasena.setMinimumHeight(44)
        card_layout.addWidget(self.txt_contrasena)

        card_layout.addSpacing(10)

        self.lbl_error = QLabel("")
        self.lbl_error.setProperty("cssClass", "error")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        card_layout.addWidget(self.lbl_error)

        card_layout.addSpacing(12)

        self.btn_iniciar_sesion = QPushButton("Iniciar Sesion")
        self.btn_iniciar_sesion.setMinimumHeight(46)
        self.btn_iniciar_sesion.setCursor(Qt.CursorShape.PointingHandCursor)
        card_layout.addWidget(self.btn_iniciar_sesion)

        card_layout.addStretch()

        layout_horizontal.addWidget(self.card)
        layout_horizontal.addStretch(1)

        self.btn_iniciar_sesion.clicked.connect(self._al_iniciar_sesion)
        self.txt_contrasena.returnPressed.connect(self._al_iniciar_sesion)
        self.txt_usuario.returnPressed.connect(
            lambda: self.txt_contrasena.setFocus()
        )

        self.txt_usuario.textChanged.connect(self._ocultar_error)
        self.txt_contrasena.textChanged.connect(self._ocultar_error)

    def _ocultar_error(self):
        if self.lbl_error.isVisible():
            self.lbl_error.setVisible(False)
            self.lbl_error.setText("")

    def _al_iniciar_sesion(self):
        username = self.txt_usuario.text().strip()
        password = self.txt_contrasena.text().strip()

        if not username or not password:
            self.mostrar_error("Usuario y contrasena son obligatorios.")
            return

        self.sesion_iniciada.emit(username, password)

    def mostrar_error(self, mensaje: str):
        self.lbl_error.setText(mensaje)
        self.lbl_error.setVisible(True)

    def limpiar(self):
        self.txt_usuario.clear()
        self.txt_contrasena.clear()
        self.lbl_error.setVisible(False)
        self.lbl_error.setText("")
