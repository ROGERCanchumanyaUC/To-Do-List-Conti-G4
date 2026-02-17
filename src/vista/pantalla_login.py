from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.vista.dialogos import mostrar_error


class PantallaLogin(QWidget):
    """Pantalla de Login (solo UI)."""

    iniciar_sesion = pyqtSignal(str, str)  # username, password

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("LoginRoot")

        self._input_usuario = QLineEdit()
        self._input_usuario.setPlaceholderText("Usuario")

        self._input_clave = QLineEdit()
        self._input_clave.setPlaceholderText("Contraseña")
        self._input_clave.setEchoMode(QLineEdit.EchoMode.Password)

        btn_ingresar = QPushButton("Ingresar")
        btn_ingresar.setObjectName("BtnPrimario")
        btn_ingresar.clicked.connect(self._on_ingresar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setObjectName("BtnSecundario")
        btn_limpiar.clicked.connect(self._on_limpiar)

        acciones = QHBoxLayout()
        acciones.addWidget(btn_limpiar)
        acciones.addWidget(btn_ingresar)

        header = QFrame()
        header.setObjectName("LoginHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(18, 18, 18, 18)

        title = QLabel("Iniciar Sesión")
        title.setObjectName("LoginTitle")

        subtitle = QLabel("Ingresa tus credenciales para entrar al Dashboard.")
        subtitle.setObjectName("LoginSubtitle")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("LoginCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)
        card_layout.addWidget(header)

        form = QWidget()
        form_layout = QGridLayout(form)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setHorizontalSpacing(12)
        form_layout.setVerticalSpacing(12)

        form_layout.addWidget(QLabel("Usuario"), 0, 0)
        form_layout.addWidget(self._input_usuario, 1, 0)

        form_layout.addWidget(QLabel("Contraseña"), 2, 0)
        form_layout.addWidget(self._input_clave, 3, 0)

        form_layout.addLayout(acciones, 4, 0)

        card_layout.addWidget(form)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.addStretch(1)

        center = QHBoxLayout()
        center.addStretch(1)
        center.addWidget(card)
        center.addStretch(1)

        root.addLayout(center)
        root.addStretch(1)

        card.setFixedWidth(420)

    def _on_limpiar(self) -> None:
        self._input_usuario.clear()
        self._input_clave.clear()
        self._input_usuario.setFocus()

    def _on_ingresar(self) -> None:
        usuario = self._input_usuario.text().strip()
        clave = self._input_clave.text()

        if not usuario or not clave:
            mostrar_error(self, "Validación", "Usuario y contraseña son obligatorios.")
            return

        self.iniciar_sesion.emit(usuario, clave)
