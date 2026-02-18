"""
Ventana principal con QStackedWidget para navegacion entre pantallas.
Indice 0: Login | Indice 1: Dashboard | Indice 2: Registrar Tarea
"""

from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.logica.login_logica import LoginLogica
from src.logica.task_manager import TaskManager
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
        self._id_usuario_actual: int | None = None

        self._login_logica = LoginLogica()
        self._task_manager = TaskManager()

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

        self.controlador_tareas = ControladorTareasVista(
            self.pantalla_dashboard,
            self.pantalla_registrar_tarea,
            task_manager=self._task_manager,
        )

        self.stack.setCurrentIndex(self.INDICE_LOGIN)

    def _conectar_senales(self):
        self.pantalla_login.sesion_iniciada.connect(self._al_iniciar_sesion)

        self.pantalla_dashboard.registrar_tarea_clicked.connect(
            self._ir_a_registrar_tarea
        )
        self.pantalla_dashboard.cerrar_sesion_clicked.connect(self._al_cerrar_sesion)

        self.pantalla_registrar_tarea.volver_clicked.connect(self._volver_a_dashboard)

    def _al_iniciar_sesion(self, username: str, password: str):
        ok = self._login_logica.login(username, password)
        if not ok:
            self.pantalla_login.mostrar_error("Credenciales incorrectas.")
            return

        id_usuario = self._login_logica.obtener_id_usuario(username)
        if id_usuario is None:
            self.pantalla_login.mostrar_error("No se encontró el usuario en la BD.")
            return

        self._usuario_actual = username
        self._id_usuario_actual = id_usuario

        self.pantalla_dashboard.establecer_usuario(username)
        self.controlador_tareas.set_usuario(id_usuario)

        self.stack.setCurrentIndex(self.INDICE_DASHBOARD)

    def _al_cerrar_sesion(self):
        self._usuario_actual = ""
        self._id_usuario_actual = None

        self.controlador_tareas.set_usuario(None)
        self.pantalla_login.limpiar()

        self.stack.setCurrentIndex(self.INDICE_LOGIN)

    def _ir_a_registrar_tarea(self):
        self.pantalla_registrar_tarea.limpiar_formulario()
        self.stack.setCurrentIndex(self.INDICE_REGISTRAR_TAREA)

    def _volver_a_dashboard(self):
        self.stack.setCurrentIndex(self.INDICE_DASHBOARD)
