# src/vista/ventana_principal.py
from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.vista.controlador_tareas_vista import ControladorTareasVista, SesionVista
from src.vista.pantalla_dashboard import PantallaDashboard
from src.vista.pantalla_login import PantallaLogin
from src.vista.pantalla_registrar_tarea import PantallaRegistrarTarea


class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("To-Do List (PyQt)")

        self._controlador = ControladorTareasVista()
        self._sesion: SesionVista | None = None

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._login = PantallaLogin()
        self._dashboard: PantallaDashboard | None = None
        self._registro: PantallaRegistrarTarea | None = None

        self._stack.addWidget(self._login)
        self._stack.setCurrentWidget(self._login)

        self._login.iniciar_sesion.connect(self._on_iniciar_sesion)

    def _on_iniciar_sesion(self, sesion: SesionVista) -> None:
        self._sesion = sesion

        self._dashboard = PantallaDashboard(sesion=sesion, controlador=self._controlador)
        self._dashboard.logout_solicitado.connect(self._on_logout)
        self._dashboard.registrar_tarea_solicitada.connect(self._abrir_registro_crear)
        self._dashboard.editar_tarea_solicitada.connect(self._abrir_registro_editar)

        self._stack.addWidget(self._dashboard)
        self._stack.setCurrentWidget(self._dashboard)

    def _on_logout(self) -> None:
        self._sesion = None

        self._login.limpiar()
        self._stack.setCurrentWidget(self._login)

        # Limpia pantallas para evitar estados colgados
        if self._dashboard is not None:
            self._stack.removeWidget(self._dashboard)
            self._dashboard.deleteLater()
            self._dashboard = None

        if self._registro is not None:
            self._stack.removeWidget(self._registro)
            self._registro.deleteLater()
            self._registro = None

    def _abrir_registro_crear(self) -> None:
        if self._sesion is None:
            return

        self._abrir_registro(task_id=None)

    def _abrir_registro_editar(self, task_id: str) -> None:
        if self._sesion is None:
            return

        self._abrir_registro(task_id=task_id)

    def _abrir_registro(self, task_id: str | None) -> None:
        # Re-crea pantalla de registro para tener estado limpio
        if self._registro is not None:
            self._stack.removeWidget(self._registro)
            self._registro.deleteLater()
            self._registro = None

        self._registro = PantallaRegistrarTarea(
            sesion=self._sesion, controlador=self._controlador, task_id=task_id
        )
        self._registro.volver_al_dashboard.connect(self._volver_dashboard)

        self._stack.addWidget(self._registro)
        self._stack.setCurrentWidget(self._registro)

    def _volver_dashboard(self) -> None:
        if self._dashboard is not None:
            self._stack.setCurrentWidget(self._dashboard)
