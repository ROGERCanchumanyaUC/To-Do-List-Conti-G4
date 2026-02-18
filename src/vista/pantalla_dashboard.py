"""
Pantalla del dashboard principal con sidebar, estadisticas y listados.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QListWidget, QListWidgetItem,
    QSizePolicy, QSpacerItem, QScrollArea
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont


class TarjetaEstadistica(QFrame):
    """Widget de card para mostrar una estadistica."""

    def __init__(self, etiqueta: str, valor: int = 0, parent=None):
        super().__init__(parent)
        self.setProperty("cssClass", "card")
        self.setMinimumWidth(160)
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(4)

        self.lbl_etiqueta = QLabel(etiqueta)
        self.lbl_etiqueta.setProperty("cssClass", "stat-etiqueta")
        layout.addWidget(self.lbl_etiqueta)

        self.lbl_valor = QLabel(str(valor))
        self.lbl_valor.setProperty("cssClass", "stat-valor")
        layout.addWidget(self.lbl_valor)

        layout.addStretch()

    def establecer_valor(self, valor: int):
        """Actualiza el valor mostrado."""
        self.lbl_valor.setText(str(valor))


class PantallaDashboard(QWidget):
    """Pantalla principal del dashboard con navegacion y estadisticas."""

    registrar_tarea_clicked = pyqtSignal()
    cerrar_sesion_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._usuario = ""
        self._configurar_ui()

    def _configurar_ui(self):
        """Configura la interfaz del dashboard."""
        layout_principal = QHBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ===== SIDEBAR =====
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(
            "QFrame { background-color: #f9f9fb; "
            "border-right: 1px solid rgba(0,0,0,0.08); }"
        )

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 24, 16, 24)
        sidebar_layout.setSpacing(4)

        # Logo / Titulo de la app
        lbl_app = QLabel("Todo App")
        fuente_app = QFont()
        fuente_app.setPointSize(16)
        fuente_app.setBold(True)
        lbl_app.setFont(fuente_app)
        lbl_app.setStyleSheet("padding: 0 8px 16px 8px;")
        sidebar_layout.addWidget(lbl_app)

        # Separador
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(
            "background-color: rgba(0,0,0,0.08); max-height: 1px;"
        )
        sidebar_layout.addWidget(sep)
        sidebar_layout.addSpacing(12)

        # Etiqueta de seccion
        lbl_nav = QLabel("NAVEGACION")
        lbl_nav.setStyleSheet(
            "font-size: 11px; font-weight: 600; color: #999999; "
            "padding: 0 8px 4px 8px; letter-spacing: 1px;"
        )
        sidebar_layout.addWidget(lbl_nav)

        # Botones de navegacion
        self.btn_dashboard = QPushButton("  Dashboard")
        self.btn_dashboard.setProperty("cssClass", "sidebar")
        self.btn_dashboard.setProperty("active", "true")
        self.btn_dashboard.setCursor(Qt.CursorShape.PointingHandCursor)
        sidebar_layout.addWidget(self.btn_dashboard)

        self.btn_registrar_tarea = QPushButton("  Registrar Tarea")
        self.btn_registrar_tarea.setProperty("cssClass", "sidebar")
        self.btn_registrar_tarea.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        sidebar_layout.addWidget(self.btn_registrar_tarea)

        self.btn_buscar = QPushButton("  Buscar")
        self.btn_buscar.setProperty("cssClass", "sidebar")
        self.btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        sidebar_layout.addWidget(self.btn_buscar)

        self.btn_completadas = QPushButton("  Completadas")
        self.btn_completadas.setProperty("cssClass", "sidebar")
        self.btn_completadas.setCursor(Qt.CursorShape.PointingHandCursor)
        sidebar_layout.addWidget(self.btn_completadas)

        sidebar_layout.addStretch()

        # Separador inferior
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(
            "background-color: rgba(0,0,0,0.08); max-height: 1px;"
        )
        sidebar_layout.addWidget(sep2)
        sidebar_layout.addSpacing(8)

        # Boton cerrar sesion
        self.btn_cerrar_sesion = QPushButton("Cerrar Sesion")
        self.btn_cerrar_sesion.setProperty("cssClass", "danger")
        self.btn_cerrar_sesion.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.btn_cerrar_sesion.setMinimumHeight(40)
        sidebar_layout.addWidget(self.btn_cerrar_sesion)

        layout_principal.addWidget(sidebar)

        # ===== CONTENIDO PRINCIPAL =====
        contenido_widget = QWidget()
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setContentsMargins(32, 28, 32, 28)
        contenido_layout.setSpacing(24)

        # --- Header ---
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        self.lbl_titulo = QLabel("Mis Tareas")
        self.lbl_titulo.setProperty("cssClass", "titulo")
        header_layout.addWidget(self.lbl_titulo)

        self.lbl_subtitulo = QLabel("Bienvenido, Usuario")
        self.lbl_subtitulo.setProperty("cssClass", "subtitulo")
        header_layout.addWidget(self.lbl_subtitulo)

        contenido_layout.addLayout(header_layout)

        # --- Tarjetas estadisticas ---
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.stat_total = TarjetaEstadistica("Total de Tareas", 0)
        stats_layout.addWidget(self.stat_total)

        self.stat_pendientes = TarjetaEstadistica("Pendientes", 0)
        stats_layout.addWidget(self.stat_pendientes)

        self.stat_completadas = TarjetaEstadistica("Completadas", 0)
        stats_layout.addWidget(self.stat_completadas)

        stats_layout.addStretch()
        contenido_layout.addLayout(stats_layout)

        # --- Listados ---
        listas_layout = QHBoxLayout()
        listas_layout.setSpacing(20)

        # Listado de tareas pendientes
        pendientes_frame = QFrame()
        pendientes_frame.setProperty("cssClass", "card")
        pendientes_v_layout = QVBoxLayout(pendientes_frame)
        pendientes_v_layout.setContentsMargins(20, 16, 20, 16)
        pendientes_v_layout.setSpacing(12)

        lbl_pendientes = QLabel("Tareas Pendientes")
        lbl_pendientes.setStyleSheet(
            "font-size: 16px; font-weight: 600;"
        )
        pendientes_v_layout.addWidget(lbl_pendientes)

        self.lista_pendientes = QListWidget()
        self.lista_pendientes.setMinimumHeight(180)
        self.lista_pendientes.setStyleSheet(
            "QListWidget { border: none; background: transparent; }"
            "QListWidget::item { padding: 10px 8px; "
            "border-bottom: 1px solid rgba(0,0,0,0.06); }"
        )
        pendientes_v_layout.addWidget(self.lista_pendientes)

        # Placeholder si esta vacio
        self.lbl_placeholder_pendientes = QLabel(
            "No hay tareas pendientes"
        )
        self.lbl_placeholder_pendientes.setProperty(
            "cssClass", "placeholder"
        )
        self.lbl_placeholder_pendientes.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        pendientes_v_layout.addWidget(self.lbl_placeholder_pendientes)

        listas_layout.addWidget(pendientes_frame)

        # Listado de tareas completadas
        completadas_frame = QFrame()
        completadas_frame.setProperty("cssClass", "card")
        completadas_v_layout = QVBoxLayout(completadas_frame)
        completadas_v_layout.setContentsMargins(20, 16, 20, 16)
        completadas_v_layout.setSpacing(12)

        lbl_completadas = QLabel("Tareas Completadas")
        lbl_completadas.setStyleSheet(
            "font-size: 16px; font-weight: 600;"
        )
        completadas_v_layout.addWidget(lbl_completadas)

        self.lista_completadas = QListWidget()
        self.lista_completadas.setMinimumHeight(180)
        self.lista_completadas.setStyleSheet(
            "QListWidget { border: none; background: transparent; }"
            "QListWidget::item { padding: 10px 8px; "
            "border-bottom: 1px solid rgba(0,0,0,0.06); }"
        )
        completadas_v_layout.addWidget(self.lista_completadas)

        # Placeholder si esta vacio
        self.lbl_placeholder_completadas = QLabel(
            "No hay tareas completadas"
        )
        self.lbl_placeholder_completadas.setProperty(
            "cssClass", "placeholder"
        )
        self.lbl_placeholder_completadas.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        completadas_v_layout.addWidget(self.lbl_placeholder_completadas)

        listas_layout.addWidget(completadas_frame)

        contenido_layout.addLayout(listas_layout)
        contenido_layout.addStretch()

        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidget(contenido_widget)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        layout_principal.addWidget(scroll, 1)

        # ===== CONEXIONES =====
        self.btn_registrar_tarea.clicked.connect(
            self.registrar_tarea_clicked.emit
        )
        self.btn_cerrar_sesion.clicked.connect(
            self.cerrar_sesion_clicked.emit
        )

    def establecer_usuario(self, usuario: str):
        """Actualiza el subtitulo con el nombre del usuario."""
        self._usuario = usuario
        self.lbl_subtitulo.setText(f"Bienvenido, {usuario}")

    def actualizar_estadisticas(
        self, total: int, pendientes: int, completadas: int
    ):
        """Actualiza los valores de las tarjetas estadisticas."""
        self.stat_total.establecer_valor(total)
        self.stat_pendientes.establecer_valor(pendientes)
        self.stat_completadas.establecer_valor(completadas)
