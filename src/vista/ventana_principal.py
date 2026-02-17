from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.vista.controlador_tareas_vista import ControladorTareasEnMemoria, UsuarioSesion
from src.vista.dialogos import mostrar_error
from src.vista.pantalla_dashboard import PantallaDashboard
from src.vista.pantalla_login import PantallaLogin


class VentanaPrincipal(QMainWindow):
    """Ventana principal: navega Login → Dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("To-Do List Conti G4")
        self.resize(1200, 720)

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._controlador = ControladorTareasEnMemoria()

        self._login = PantallaLogin()
        self._login.iniciar_sesion.connect(self._on_iniciar_sesion)

        self._dashboard: PantallaDashboard | None = None

        self._stack.addWidget(self._login)
        self._stack.setCurrentWidget(self._login)

    def _on_iniciar_sesion(self, username: str, password: str) -> None:
        # Solo UI: validamos que no estén vacíos (lógica real vendrá después)
        if not username.strip() or not password:
            mostrar_error(self, "Validación", "Usuario y contraseña son obligatorios.")
            return

        sesion = UsuarioSesion(id_usuario=1, username=username.strip())

        self._dashboard = PantallaDashboard(sesion=sesion, controlador=self._controlador)
        self._stack.addWidget(self._dashboard)
        self._stack.setCurrentWidget(self._dashboard)
