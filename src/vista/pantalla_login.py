# src/vista/pantalla_login.py
from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.vista.controlador_tareas_vista import SesionVista


class PantallaLogin(QWidget):
    iniciar_sesion = pyqtSignal(SesionVista)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("LoginRoot")

        self._input_usuario = QLineEdit()
        self._input_password = QLineEdit()
        self._btn_ingresar = QPushButton("Iniciar sesión")

        self._construir_ui()
        self._conectar_eventos()

    def _construir_ui(self) -> None:
        layout_root = QVBoxLayout(self)
        layout_root.setContentsMargins(24, 24, 24, 24)

        layout_root.addStretch(1)

        card = QFrame()
        card.setObjectName("LoginCard")
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        card.setFixedWidth(420)

        layout_card = QVBoxLayout(card)
        layout_card.setContentsMargins(26, 26, 26, 26)
        layout_card.setSpacing(14)

        titulo = QLabel("Ingresar")
        titulo.setObjectName("TituloGrande")

        subtitulo = QLabel("Accede para gestionar tus tareas.")
        subtitulo.setObjectName("Subtitulo")

        self._input_usuario.setPlaceholderText("Usuario")
        self._input_password.setPlaceholderText("Contraseña")
        self._input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self._btn_ingresar.setObjectName("BotonPrimario")

        layout_card.addWidget(titulo)
        layout_card.addWidget(subtitulo)
        layout_card.addSpacing(8)
        layout_card.addWidget(self._input_usuario)
        layout_card.addWidget(self._input_password)
        layout_card.addSpacing(8)
        layout_card.addWidget(self._btn_ingresar)

        row_center = QHBoxLayout()
        row_center.addStretch(1)
        row_center.addWidget(card)
        row_center.addStretch(1)

        layout_root.addLayout(row_center)
        layout_root.addStretch(2)

    def _conectar_eventos(self) -> None:
        self._btn_ingresar.clicked.connect(self._on_ingresar)
        self._input_password.returnPressed.connect(self._on_ingresar)

    def _on_ingresar(self) -> None:
        usuario = (self._input_usuario.text() or "").strip()
        password = (self._input_password.text() or "").strip()

        if not usuario:
            QMessageBox.warning(self, "Validación", "El usuario no puede estar vacío.")
            self._input_usuario.setFocus()
            return

        if not password:
            QMessageBox.warning(self, "Validación", "La contraseña no puede estar vacía.")
            self._input_password.setFocus()
            return

        self.iniciar_sesion.emit(SesionVista(username=usuario))

    def limpiar(self) -> None:
        self._input_usuario.clear()
        self._input_password.clear()
        self._input_usuario.setFocus()
