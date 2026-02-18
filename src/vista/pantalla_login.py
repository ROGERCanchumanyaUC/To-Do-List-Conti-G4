"""
Pantalla de inicio de sesion con fondo degradado y card centrado.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


class PantallaLogin(QWidget):
    """Pantalla de login a pantalla completa con card centrado."""

    sesion_iniciada = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("cssClass", "login-fondo")
        self._configurar_ui()

    def _configurar_ui(self):
        """Configura la interfaz de la pantalla de login."""
        # Layout principal que centra el card
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # Contenedor horizontal para centrar
        layout_horizontal = QHBoxLayout()
        layout_horizontal.setContentsMargins(0, 0, 0, 0)

        # Espaciadores para centrar vertical y horizontalmente
        layout_principal.addStretch(1)
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addStretch(1)

        layout_horizontal.addStretch(1)

        # Card de login
        self.card = QFrame()
        self.card.setProperty("cssClass", "login-card")
        self.card.setFixedWidth(420)
        self.card.setMaximumHeight(520)
        self.card.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred
        )

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 44, 40, 40)
        card_layout.setSpacing(8)

        # Icono / Branding
        lbl_icono = QLabel("\u2713")
        lbl_icono.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fuente_icono = QFont()
        fuente_icono.setPointSize(28)
        fuente_icono.setBold(True)
        lbl_icono.setFont(fuente_icono)
        card_layout.addWidget(lbl_icono)

        card_layout.addSpacing(4)

        # Titulo
        lbl_titulo = QLabel("Iniciar Sesion")
        lbl_titulo.setProperty("cssClass", "titulo")
        lbl_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_titulo)

        # Subtitulo
        lbl_subtitulo = QLabel("Ingresa tus credenciales para continuar")
        lbl_subtitulo.setProperty("cssClass", "subtitulo")
        lbl_subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(lbl_subtitulo)

        card_layout.addSpacing(24)

        # Campo: Usuario
        lbl_usuario = QLabel("Usuario")
        lbl_usuario.setStyleSheet("font-weight: 500; font-size: 13px;")
        card_layout.addWidget(lbl_usuario)

        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Ingresa tu usuario")
        self.txt_usuario.setMinimumHeight(44)
        card_layout.addWidget(self.txt_usuario)

        card_layout.addSpacing(12)

        # Campo: Contrasena
        lbl_contrasena = QLabel("Contrasena")
        lbl_contrasena.setStyleSheet("font-weight: 500; font-size: 13px;")
        card_layout.addWidget(lbl_contrasena)

        self.txt_contrasena = QLineEdit()
        self.txt_contrasena.setPlaceholderText("Ingresa tu contrasena")
        self.txt_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_contrasena.setMinimumHeight(44)
        card_layout.addWidget(self.txt_contrasena)

        card_layout.addSpacing(8)

        # Label de error (oculto por defecto)
        self.lbl_error = QLabel("")
        self.lbl_error.setProperty("cssClass", "error")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setVisible(False)
        self.lbl_error.setWordWrap(True)
        card_layout.addWidget(self.lbl_error)

        card_layout.addSpacing(8)

        # Boton: Iniciar sesion
        self.btn_iniciar_sesion = QPushButton("Iniciar Sesion")
        self.btn_iniciar_sesion.setMinimumHeight(46)
        self.btn_iniciar_sesion.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        card_layout.addWidget(self.btn_iniciar_sesion)

        card_layout.addStretch()

        layout_horizontal.addWidget(self.card)
        layout_horizontal.addStretch(1)

        # Conectar senal del boton (mock: emite usuario sin validar)
        self.btn_iniciar_sesion.clicked.connect(self._al_iniciar_sesion)
        self.txt_contrasena.returnPressed.connect(self._al_iniciar_sesion)

    def _al_iniciar_sesion(self):
        """Emite la senal sesion_iniciada con el nombre de usuario (mock)."""
        usuario = self.txt_usuario.text().strip()
        if not usuario:
            usuario = "Usuario"
        self.sesion_iniciada.emit(usuario)

    def mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error en el label."""
        self.lbl_error.setText(mensaje)
        self.lbl_error.setVisible(True)

    def limpiar(self):
        """Limpia los campos del formulario."""
        self.txt_usuario.clear()
        self.txt_contrasena.clear()
        self.lbl_error.setVisible(False)
        self.lbl_error.setText("")
