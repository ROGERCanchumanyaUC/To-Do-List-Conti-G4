"""
Ventana principal con QStackedWidget para navegacion entre pantallas.
Indice 0: Login | Indice 1: Dashboard | Indice 2: Registrar Tarea
"""

from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.vista.pantalla_login import PantallaLogin
from src.vista.pantalla_dashboard import PantallaDashboard
from src.vista.pantalla_registrar_tarea import PantallaRegistrarTarea
from src.vista.controlador_tareas_vista import ControladorTareasVista


class VentanaPrincipal(QMainWindow):
    """Ventana principal que gestiona la navegacion entre pantallas."""

    INDICE_LOGIN = 0
    INDICE_DASHBOARD = 1
    INDICE_REGISTRAR_TAREA = 2

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo App - Gestor de Tareas")
        self.setMinimumSize(1024, 680)
        self._usuario_actual = ""
        self._configurar_ui()
        self._conectar_senales()

    def _configurar_ui(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.pantalla_login = PantallaLogin()
        self.stack.addWidget(self.pantalla_login)

        self.pantalla_dashboard = PantallaDashboard()
        self.stack.addWidget(self.pantalla_dashboard)

        self.pantalla_registrar_tarea = PantallaRegistrarTarea()
        self.stack.addWidget(self.pantalla_registrar_tarea)

        # El controlador ahora recibe ambas vistas
        self.controlador_tareas = ControladorTareasVista(
            self.pantalla_dashboard,
            self.pantalla_registrar_tarea,
        )

        self.stack.setCurrentIndex(self.INDICE_LOGIN)

    def _conectar_senales(self):
        # Login -> Dashboard
        self.pantalla_login.sesion_iniciada.connect(
            self._al_iniciar_sesion
        )

        # Dashboard -> Registrar Tarea
        self.pantalla_dashboard.registrar_tarea_clicked.connect(
            self._ir_a_registrar_tarea
        )

        # Dashboard -> Login (cerrar sesion)
        self.pantalla_dashboard.cerrar_sesion_clicked.connect(
            self._al_cerrar_sesion
        )

        # Registrar Tarea -> Dashboard (volver)
        self.pantalla_registrar_tarea.volver_clicked.connect(
            self._volver_a_dashboard
        )

    def _al_iniciar_sesion(self, usuario: str):
        self._usuario_actual = usuario
        self.pantalla_dashboard.establecer_usuario(usuario)
        self.stack.setCurrentIndex(self.INDICE_DASHBOARD)

    def _al_cerrar_sesion(self):
        self._usuario_actual = ""
        self.pantalla_login.limpiar()
        self.stack.setCurrentIndex(self.INDICE_LOGIN)

    def _ir_a_registrar_tarea(self):
        self.pantalla_registrar_tarea.limpiar_formulario()
        self.stack.setCurrentIndex(self.INDICE_REGISTRAR_TAREA)

    def _volver_a_dashboard(self):
        self.stack.setCurrentIndex(self.INDICE_DASHBOARD)
