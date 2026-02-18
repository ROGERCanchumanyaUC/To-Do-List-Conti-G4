"""
Pantalla del dashboard principal - sin sidebar, con toolbar centrado.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QScrollArea,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QColor


class TarjetaEstadistica(QFrame):
    """Widget de card para mostrar una estadistica con icono."""

    def __init__(
        self,
        etiqueta: str,
        valor: int = 0,
        icono: str = "",
        color_icono: str = "#0f3460",
        parent=None,
    ):
        super().__init__(parent)
        self.setProperty("cssClass", "stat-card")
        self.setMinimumWidth(200)
        self.setFixedHeight(120)

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(24)
        sombra.setOffset(0, 4)
        sombra.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(sombra)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(4)

        top_row = QHBoxLayout()
        top_row.setSpacing(0)

        self.lbl_etiqueta = QLabel(etiqueta.upper())
        self.lbl_etiqueta.setProperty("cssClass", "stat-etiqueta")
        top_row.addWidget(self.lbl_etiqueta)

        top_row.addStretch()

        lbl_icono = QLabel(icono)
        lbl_icono.setStyleSheet(f"font-size: 22px; color: {color_icono};")
        top_row.addWidget(lbl_icono)

        layout.addLayout(top_row)
        layout.addSpacing(8)

        self.lbl_valor = QLabel(str(valor))
        self.lbl_valor.setProperty("cssClass", "stat-valor")
        layout.addWidget(self.lbl_valor)

        layout.addStretch()

    def establecer_valor(self, valor: int):
        self.lbl_valor.setText(str(valor))


class TarjetaTarea(QFrame):
    """Card individual para mostrar una tarea."""

    completar_clicked = pyqtSignal(int)
    editar_clicked = pyqtSignal(int)
    eliminar_clicked = pyqtSignal(int)

    def __init__(
        self,
        id_tarea: int,
        titulo: str,
        descripcion: str,
        fecha: str,
        es_completada: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self._id_tarea = id_tarea
        self.setProperty("cssClass", "task-card")
        self.setCursor(Qt.CursorShape.ArrowCursor)

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(16)
        sombra.setOffset(0, 2)
        sombra.setColor(QColor(0, 0, 0, 10))
        self.setGraphicsEffect(sombra)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        # Fila superior: titulo + fecha
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        lbl_titulo = QLabel(titulo)
        lbl_titulo.setProperty("cssClass", "task-titulo")
        lbl_titulo.setWordWrap(True)
        top_row.addWidget(lbl_titulo, 1)

        lbl_fecha = QLabel(fecha)
        lbl_fecha.setProperty("cssClass", "task-fecha")
        lbl_fecha.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )
        top_row.addWidget(lbl_fecha)

        layout.addLayout(top_row)

        # Descripcion
        if descripcion:
            lbl_desc = QLabel(descripcion)
            lbl_desc.setProperty("cssClass", "task-descripcion")
            lbl_desc.setWordWrap(True)
            lbl_desc.setMaximumHeight(50)
            layout.addWidget(lbl_desc)

        layout.addSpacing(8)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addStretch()

        # Botones para tareas pendientes
        if not es_completada:
            btn_completar = QPushButton("Completar")
            btn_completar.setProperty("cssClass", "action-completar")
            btn_completar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_completar.setFixedHeight(32)
            btn_completar.clicked.connect(
                lambda: self.completar_clicked.emit(self._id_tarea)
            )
            btn_row.addWidget(btn_completar)

            btn_editar = QPushButton("Editar")
            btn_editar.setProperty("cssClass", "action-editar")
            btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_editar.setFixedHeight(32)
            btn_editar.clicked.connect(
                lambda: self.editar_clicked.emit(self._id_tarea)
            )
            btn_row.addWidget(btn_editar)

            layout.addLayout(btn_row)
            return

        # Botón Eliminar solo para tareas completadas
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setProperty("cssClass", "danger")
        btn_eliminar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_eliminar.setFixedHeight(32)
        btn_eliminar.clicked.connect(
            lambda: self.eliminar_clicked.emit(self._id_tarea)
        )
        btn_row.addWidget(btn_eliminar)

        layout.addLayout(btn_row)


class PantallaDashboard(QWidget):
    """Pantalla principal del dashboard sin sidebar."""

    registrar_tarea_clicked = pyqtSignal()
    cerrar_sesion_clicked = pyqtSignal()
    buscar_clicked = pyqtSignal(str)
    completar_tarea_clicked = pyqtSignal(int)
    editar_tarea_clicked = pyqtSignal(int)
    eliminar_tarea_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._usuario = ""
        self._configurar_ui()

    def _configurar_ui(self):
        layout_raiz = QVBoxLayout(self)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # ===== TOP BAR =====
        topbar = QFrame()
        topbar.setProperty("cssClass", "header-bar")
        topbar.setFixedHeight(68)

        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(32, 0, 32, 0)
        topbar_layout.setSpacing(12)

        self.lbl_usuario = QLabel("Dashboard")
        self.lbl_usuario.setStyleSheet(
            "font-size: 18px; font-weight: 700; color: #ffffff;"
        )
        topbar_layout.addWidget(self.lbl_usuario)

        topbar_layout.addStretch()

        # Centro: Registrar Tarea + Buscar
        centro_layout = QHBoxLayout()
        centro_layout.setSpacing(10)

        self.btn_registrar_tarea = QPushButton("Registrar Tarea")
        self.btn_registrar_tarea.setProperty("cssClass", "toolbar")
        self.btn_registrar_tarea.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_registrar_tarea.setFixedHeight(42)
        centro_layout.addWidget(self.btn_registrar_tarea)

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setProperty("cssClass", "search")
        self.txt_buscar.setPlaceholderText("Buscar tarea por nombre...")
        self.txt_buscar.setFixedHeight(42)
        self.txt_buscar.setMinimumWidth(260)
        centro_layout.addWidget(self.txt_buscar)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setProperty("cssClass", "toolbar")
        self.btn_buscar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_buscar.setFixedHeight(42)
        centro_layout.addWidget(self.btn_buscar)

        topbar_layout.addLayout(centro_layout)

        topbar_layout.addStretch()

        self.btn_cerrar_sesion = QPushButton("Cerrar Sesion")
        self.btn_cerrar_sesion.setProperty("cssClass", "logout")
        self.btn_cerrar_sesion.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cerrar_sesion.setFixedHeight(42)
        topbar_layout.addWidget(self.btn_cerrar_sesion)

        layout_raiz.addWidget(topbar)

        # ===== SCROLL AREA PARA CONTENIDO =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(
            "QScrollArea { border: none; background: qlineargradient("
            "x1:0, y1:0, x2:1, y2:1, stop:0 #dbeafe, stop:1 #ffffff); }"
        )

        contenido_widget = QWidget()
        contenido_widget.setStyleSheet(
            "background: qlineargradient("
            "x1:0, y1:0, x2:1, y2:1, stop:0 #dbeafe, stop:1 #ffffff);"
        )
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setContentsMargins(40, 32, 40, 32)
        contenido_layout.setSpacing(0)

        self.lbl_titulo = QLabel("Dashboard")
        self.lbl_titulo.setProperty("cssClass", "titulo")
        contenido_layout.addWidget(self.lbl_titulo)

        contenido_layout.addSpacing(4)

        self.lbl_subtitulo = QLabel("Bienvenido, Usuario")
        self.lbl_subtitulo.setProperty("cssClass", "subtitulo")
        contenido_layout.addWidget(self.lbl_subtitulo)

        contenido_layout.addSpacing(28)

        # ===== ESTADISTICAS =====
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.stat_total = TarjetaEstadistica(
            "Total de Tareas", 0, icono="\u2630", color_icono="#1d4ed8"
        )
        stats_layout.addWidget(self.stat_total)

        self.stat_pendientes = TarjetaEstadistica(
            "Pendientes", 0, icono="\u25cb", color_icono="#d97706"
        )
        stats_layout.addWidget(self.stat_pendientes)

        self.stat_completadas = TarjetaEstadistica(
            "Completadas", 0, icono="\u2713", color_icono="#16a34a"
        )
        stats_layout.addWidget(self.stat_completadas)

        stats_layout.addStretch()
        contenido_layout.addLayout(stats_layout)

        contenido_layout.addSpacing(32)

        # ===== SECCION TAREAS PENDIENTES =====
        lbl_pendientes = QLabel("Tareas Pendientes")
        lbl_pendientes.setProperty("cssClass", "section-title")
        contenido_layout.addWidget(lbl_pendientes)

        contenido_layout.addSpacing(14)

        self.contenedor_pendientes = QVBoxLayout()
        self.contenedor_pendientes.setSpacing(10)
        contenido_layout.addLayout(self.contenedor_pendientes)

        self.lbl_placeholder_pendientes = QLabel("No hay tareas pendientes")
        self.lbl_placeholder_pendientes.setProperty("cssClass", "placeholder")
        self.lbl_placeholder_pendientes.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        contenido_layout.addWidget(self.lbl_placeholder_pendientes)

        contenido_layout.addSpacing(36)

        # ===== SECCION TAREAS COMPLETADAS =====
        lbl_completadas = QLabel("Tareas Completadas")
        lbl_completadas.setProperty("cssClass", "section-title")
        contenido_layout.addWidget(lbl_completadas)

        contenido_layout.addSpacing(14)

        self.contenedor_completadas = QVBoxLayout()
        self.contenedor_completadas.setSpacing(10)
        contenido_layout.addLayout(self.contenedor_completadas)

        self.lbl_placeholder_completadas = QLabel("No hay tareas completadas")
        self.lbl_placeholder_completadas.setProperty("cssClass", "placeholder")
        self.lbl_placeholder_completadas.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        contenido_layout.addWidget(self.lbl_placeholder_completadas)

        contenido_layout.addStretch()

        scroll.setWidget(contenido_widget)
        layout_raiz.addWidget(scroll, 1)

        # ===== CONEXIONES =====
        self.btn_registrar_tarea.clicked.connect(
            self.registrar_tarea_clicked.emit
        )
        self.btn_cerrar_sesion.clicked.connect(
            self.cerrar_sesion_clicked.emit
        )
        self.btn_buscar.clicked.connect(self._al_buscar)
        self.txt_buscar.returnPressed.connect(self._al_buscar)

    def _al_buscar(self):
        texto = self.txt_buscar.text().strip()
        self.buscar_clicked.emit(texto)

    def establecer_usuario(self, usuario: str):
        self._usuario = usuario
        self.lbl_subtitulo.setText(
            f"Bienvenido, {usuario}. Aqui tienes un resumen de tus tareas."
        )

    def actualizar_estadisticas(self, total: int, pendientes: int, completadas: int):
        self.stat_total.establecer_valor(total)
        self.stat_pendientes.establecer_valor(pendientes)
        self.stat_completadas.establecer_valor(completadas)

    def mostrar_tareas(self, tareas: list):
        """Muestra las tareas como cards en las secciones correspondientes."""
        self._limpiar_layout(self.contenedor_pendientes)
        self._limpiar_layout(self.contenedor_completadas)

        pendientes = [t for t in tareas if not t["completada"]]
        completadas = [t for t in tareas if t["completada"]]

        self.lbl_placeholder_pendientes.setVisible(len(pendientes) == 0)
        for tarea in pendientes:
            card = TarjetaTarea(
                id_tarea=tarea["id_tarea"],
                titulo=tarea["titulo"],
                descripcion=tarea["descripcion"],
                fecha=tarea["creada_en"],
                es_completada=False,
            )
            card.completar_clicked.connect(self.completar_tarea_clicked.emit)
            card.editar_clicked.connect(self.editar_tarea_clicked.emit)
            self.contenedor_pendientes.addWidget(card)

        self.lbl_placeholder_completadas.setVisible(len(completadas) == 0)
        for tarea in completadas:
            card = TarjetaTarea(
                id_tarea=tarea["id_tarea"],
                titulo=tarea["titulo"],
                descripcion=tarea["descripcion"],
                fecha=tarea["creada_en"],
                es_completada=True,
            )
            card.eliminar_clicked.connect(self.eliminar_tarea_clicked.emit)
            self.contenedor_completadas.addWidget(card)

    def _limpiar_layout(self, layout):
        """Elimina todos los widgets de un layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
