"""
Pantalla del dashboard principal.
Top bar con Cerrar Sesion a la derecha, Registrar Tarea + Buscar centrados.
Secciones con fondos coloreados y tarjetas animadas.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QLineEdit,
    QScrollArea,
)
from PyQt6.QtCore import pyqtSignal, Qt

from src.vista.animaciones import BotonAnimado, TarjetaAnimada


# ------------------------------------------------------------------ #
#  TARJETA DE ESTADISTICA (con color propio)
# ------------------------------------------------------------------ #

class TarjetaEstadistica(TarjetaAnimada):
    """Card para mostrar una estadistica con icono y color propio."""

    def __init__(
        self,
        etiqueta: str,
        valor: int = 0,
        icono: str = "",
        variante: str = "blue",
        parent=None,
    ):
        # Sombra tintada segun variante
        colores_sombra = {
            "blue": "#2563eb",
            "amber": "#d97706",
            "green": "#16a34a",
        }
        super().__init__(
            color_sombra=colores_sombra.get(variante, "#000000"),
            intensidad=25,
            blur_reposo=6.0,
            blur_hover=24.0,
            parent=parent,
        )

        self.setProperty("cssClass", f"stat-{variante}")
        self.setMinimumWidth(210)
        self.setFixedHeight(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 22, 26, 22)
        layout.setSpacing(4)

        top_row = QHBoxLayout()
        top_row.setSpacing(0)

        self.lbl_etiqueta = QLabel(etiqueta.upper())
        self.lbl_etiqueta.setProperty("cssClass", "stat-etiqueta")
        top_row.addWidget(self.lbl_etiqueta)

        top_row.addStretch()

        lbl_icono = QLabel(icono)
        lbl_icono.setProperty("cssClass", f"stat-icono-{variante}")
        top_row.addWidget(lbl_icono)

        layout.addLayout(top_row)
        layout.addSpacing(10)

        self.lbl_valor = QLabel(str(valor))
        self.lbl_valor.setProperty("cssClass", f"stat-valor-{variante}")
        layout.addWidget(self.lbl_valor)

        layout.addStretch()

    def establecer_valor(self, valor: int):
        self.lbl_valor.setText(str(valor))


# ------------------------------------------------------------------ #
#  TARJETA DE TAREA (con borde lateral coloreado)
# ------------------------------------------------------------------ #

class TarjetaTarea(TarjetaAnimada):
    """Card para mostrar una tarea con animacion de elevacion."""

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
        color_s = "#16a34a" if es_completada else "#d97706"
        super().__init__(
            color_sombra=color_s,
            intensidad=18,
            blur_reposo=4.0,
            blur_hover=20.0,
            parent=parent,
        )

        self._id_tarea = id_tarea
        css_card = "task-card-completada" if es_completada else "task-card-pendiente"
        self.setProperty("cssClass", css_card)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 18, 22, 18)
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

        layout.addSpacing(10)

        # Botones
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        if not es_completada:
            btn_completar = BotonAnimado(
                "Completar",
                color_sombra="#16a34a",
                intensidad_sombra=50,
                blur_reposo=0,
                blur_hover=14.0,
            )
            btn_completar.setProperty("cssClass", "btn-completar")
            btn_completar.setFixedHeight(34)
            btn_completar.setStyleSheet(
                "QPushButton { background-color: #bbf7d0; color: #1a1a2e;"
                " border: none; border-radius: 10px; padding: 7px 20px;"
                " font-size: 12.5px; font-weight: 700; }"
                "QPushButton:hover { background-color: #86efac; }"
                "QPushButton:pressed { background-color: #4ade80; }"
            )
            btn_completar.clicked.connect(
                lambda: self.completar_clicked.emit(self._id_tarea)
            )
            btn_row.addWidget(btn_completar)

            btn_editar = BotonAnimado(
                "Editar",
                color_sombra="#d97706",
                intensidad_sombra=50,
                blur_reposo=0,
                blur_hover=14.0,
            )
            btn_editar.setProperty("cssClass", "btn-editar")
            btn_editar.setFixedHeight(34)
            btn_editar.setStyleSheet(
                "QPushButton { background-color: #fde68a; color: #1a1a2e;"
                " border: none; border-radius: 10px; padding: 7px 20px;"
                " font-size: 12.5px; font-weight: 700; }"
                "QPushButton:hover { background-color: #fcd34d; }"
                "QPushButton:pressed { background-color: #fbbf24; }"
            )
            btn_editar.clicked.connect(
                lambda: self.editar_clicked.emit(self._id_tarea)
            )
            btn_row.addWidget(btn_editar)
        else:
            btn_eliminar = BotonAnimado(
                "Eliminar",
                color_sombra="#dc2626",
                intensidad_sombra=50,
                blur_reposo=0,
                blur_hover=14.0,
            )
            btn_eliminar.setProperty("cssClass", "btn-eliminar")
            btn_eliminar.setFixedHeight(34)
            btn_eliminar.setStyleSheet(
                "QPushButton { background-color: #fecaca; color: #1a1a2e;"
                " border: none; border-radius: 10px; padding: 7px 20px;"
                " font-size: 12.5px; font-weight: 700; }"
                "QPushButton:hover { background-color: #fca5a5; }"
                "QPushButton:pressed { background-color: #f87171; }"
            )
            btn_eliminar.clicked.connect(
                lambda: self.eliminar_clicked.emit(self._id_tarea)
            )
            btn_row.addWidget(btn_eliminar)

        layout.addLayout(btn_row)


# ------------------------------------------------------------------ #
#  DASHBOARD PRINCIPAL
# ------------------------------------------------------------------ #

class PantallaDashboard(QWidget):
    """Pantalla principal del dashboard."""

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

        # ============ TOP BAR ============
        topbar = QFrame()
        topbar.setProperty("cssClass", "header-bar")
        topbar.setFixedHeight(72)

        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(36, 0, 36, 0)
        topbar_layout.setSpacing(16)

        # Titulo izquierda
        self.lbl_usuario = QLabel("Dashboard")
        self.lbl_usuario.setStyleSheet(
            "font-size: 20px; font-weight: 800; color: #ffffff;"
            "letter-spacing: -0.3px;"
        )
        topbar_layout.addWidget(self.lbl_usuario)

        topbar_layout.addStretch()

        # Centro: Registrar Tarea + Buscar
        centro = QHBoxLayout()
        centro.setSpacing(12)

        self.btn_registrar_tarea = BotonAnimado(
            "Registrar Tarea",
            color_sombra="#4f46e5",
            intensidad_sombra=70,
            blur_reposo=2.0,
            blur_hover=16.0,
        )
        self.btn_registrar_tarea.setProperty("cssClass", "btn-registrar")
        self.btn_registrar_tarea.setFixedHeight(44)
        centro.addWidget(self.btn_registrar_tarea)

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setProperty("cssClass", "search")
        self.txt_buscar.setPlaceholderText("Buscar tarea por nombre...")
        self.txt_buscar.setFixedHeight(44)
        self.txt_buscar.setMinimumWidth(280)
        centro.addWidget(self.txt_buscar)

        self.btn_buscar = BotonAnimado(
            "Buscar",
            color_sombra="#0891b2",
            intensidad_sombra=70,
            blur_reposo=2.0,
            blur_hover=16.0,
        )
        self.btn_buscar.setProperty("cssClass", "btn-buscar")
        self.btn_buscar.setFixedHeight(44)
        centro.addWidget(self.btn_buscar)

        topbar_layout.addLayout(centro)

        topbar_layout.addStretch()

        # Derecha: Cerrar Sesion
        self.btn_cerrar_sesion = BotonAnimado(
            "Cerrar Sesion",
            color_sombra="#dc2626",
            intensidad_sombra=70,
            blur_reposo=2.0,
            blur_hover=16.0,
        )
        self.btn_cerrar_sesion.setProperty("cssClass", "btn-logout")
        self.btn_cerrar_sesion.setFixedHeight(44)
        topbar_layout.addWidget(self.btn_cerrar_sesion)

        layout_raiz.addWidget(topbar)

        # ============ SCROLL AREA ============
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: #e8ecf1; }")

        contenido_widget = QWidget()
        contenido_widget.setStyleSheet("background: #e8ecf1;")
        contenido_layout = QVBoxLayout(contenido_widget)
        contenido_layout.setContentsMargins(44, 36, 44, 36)
        contenido_layout.setSpacing(0)

        # Titulo + Subtitulo
        self.lbl_titulo = QLabel("Dashboard")
        self.lbl_titulo.setProperty("cssClass", "titulo")
        contenido_layout.addWidget(self.lbl_titulo)

        contenido_layout.addSpacing(4)

        self.lbl_subtitulo = QLabel("Bienvenido, Usuario")
        self.lbl_subtitulo.setProperty("cssClass", "subtitulo")
        contenido_layout.addWidget(self.lbl_subtitulo)

        contenido_layout.addSpacing(30)

        # ============ ESTADISTICAS ============
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(18)

        self.stat_total = TarjetaEstadistica(
            "Total de Tareas", 0, icono="\u2630", variante="blue"
        )
        stats_layout.addWidget(self.stat_total)

        self.stat_pendientes = TarjetaEstadistica(
            "Pendientes", 0, icono="\u25cb", variante="amber"
        )
        stats_layout.addWidget(self.stat_pendientes)

        self.stat_completadas = TarjetaEstadistica(
            "Completadas", 0, icono="\u2713", variante="green"
        )
        stats_layout.addWidget(self.stat_completadas)

        stats_layout.addStretch()
        contenido_layout.addLayout(stats_layout)

        contenido_layout.addSpacing(36)

        # ============ SECCION TAREAS PENDIENTES ============
        self.frame_pendientes = QFrame()
        self.frame_pendientes.setProperty("cssClass", "section-pendientes")
        frame_pend_layout = QVBoxLayout(self.frame_pendientes)
        frame_pend_layout.setContentsMargins(24, 22, 24, 24)
        frame_pend_layout.setSpacing(0)

        header_pend = QHBoxLayout()
        lbl_pendientes = QLabel("\u25cb  Tareas Pendientes")
        lbl_pendientes.setProperty("cssClass", "section-title-amber")
        header_pend.addWidget(lbl_pendientes)
        header_pend.addStretch()
        frame_pend_layout.addLayout(header_pend)

        frame_pend_layout.addSpacing(16)

        self.contenedor_pendientes = QVBoxLayout()
        self.contenedor_pendientes.setSpacing(12)
        frame_pend_layout.addLayout(self.contenedor_pendientes)

        self.lbl_placeholder_pendientes = QLabel("No hay tareas pendientes")
        self.lbl_placeholder_pendientes.setProperty("cssClass", "placeholder")
        self.lbl_placeholder_pendientes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_pend_layout.addWidget(self.lbl_placeholder_pendientes)

        contenido_layout.addWidget(self.frame_pendientes)

        contenido_layout.addSpacing(28)

        # ============ SECCION TAREAS COMPLETADAS ============
        self.frame_completadas = QFrame()
        self.frame_completadas.setProperty("cssClass", "section-completadas")
        frame_comp_layout = QVBoxLayout(self.frame_completadas)
        frame_comp_layout.setContentsMargins(24, 22, 24, 24)
        frame_comp_layout.setSpacing(0)

        header_comp = QHBoxLayout()
        lbl_completadas = QLabel("\u2713  Tareas Completadas")
        lbl_completadas.setProperty("cssClass", "section-title-green")
        header_comp.addWidget(lbl_completadas)
        header_comp.addStretch()
        frame_comp_layout.addLayout(header_comp)

        frame_comp_layout.addSpacing(16)

        self.contenedor_completadas = QVBoxLayout()
        self.contenedor_completadas.setSpacing(12)
        frame_comp_layout.addLayout(self.contenedor_completadas)

        self.lbl_placeholder_completadas = QLabel("No hay tareas completadas")
        self.lbl_placeholder_completadas.setProperty("cssClass", "placeholder")
        self.lbl_placeholder_completadas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_comp_layout.addWidget(self.lbl_placeholder_completadas)

        contenido_layout.addWidget(self.frame_completadas)

        contenido_layout.addStretch()

        scroll.setWidget(contenido_widget)
        layout_raiz.addWidget(scroll, 1)

        # ============ CONEXIONES ============
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
        """Muestra las tareas como cards animadas en las secciones."""
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
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
