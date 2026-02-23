"""
Pantalla del dashboard principal.
Top bar con Cerrar Sesion a la derecha, Registrar Tarea + Buscar centrados.
Secciones con fondos coloreados y tarjetas animadas.

HU08 (UI): Filtrar por estado desde las tarjetas de estadística:
- Click en TOTAL -> muestra ambas columnas (Pendientes izq, Completadas der)
- Click en PENDIENTES -> muestra solo Pendientes (en columna izquierda), mantiene ancho 2 columnas
- Click en COMPLETADAS -> muestra solo Completadas (en columna izquierda), mantiene ancho 2 columnas

HU10 (UI): Ordenar tareas:
- Botón Ordenar ▾ (a la derecha de Buscar) -> Por fecha / Por nombre
- Emite ordenar_changed("fecha"|"nombre")
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QLineEdit,
    QScrollArea,
    QMenu,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction, QActionGroup

from src.vista.animaciones import BotonAnimado, TarjetaAnimada


# ------------------------------------------------------------------ #
#  TARJETA DE ESTADISTICA (clicable + color propio)
# ------------------------------------------------------------------ #

class TarjetaEstadistica(TarjetaAnimada):
    """Card para mostrar una estadistica con icono y color propio (clicable)."""

    clicked = pyqtSignal()

    def __init__(
        self,
        etiqueta: str,
        valor: int = 0,
        icono: str = "",
        variante: str = "blue",
        parent=None,
    ):
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.unsetCursor()
        super().leaveEvent(event)


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

    # HU08
    filtro_total_clicked = pyqtSignal()
    filtro_pendientes_clicked = pyqtSignal()
    filtro_completadas_clicked = pyqtSignal()

    # HU10
    ordenar_changed = pyqtSignal(str)  # "fecha" | "nombre"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._usuario = ""
        self._modo_filtro = "total"
        self._modo_orden = "fecha"
        self._configurar_ui()

    # -------------------- HU08: mover cuadros para que "solo uno" aparezca a la izquierda --------------------

    def _mover_a_layout(self, widget: QWidget, layout: QVBoxLayout) -> None:
        """Mueve widget al layout objetivo (solo si no está ya ahí)."""
        if widget.parent() is layout.parentWidget():
            return
        # Quita de su layout anterior si aplica
        if widget.parent() is not None and widget.parent() is not self:
            # remover del layout anterior sin destruir
            old_parent = widget.parent()
            old_layout = old_parent.layout()
            if old_layout is not None:
                old_layout.removeWidget(widget)
        layout.addWidget(widget)

    def aplicar_modo_filtro(self, modo: str) -> None:
        modo = (modo or "total").strip().lower()
        if modo not in ("total", "pendientes", "completadas"):
            modo = "total"
        self._modo_filtro = modo

        if modo == "total":
            # Pendientes a la izquierda, Completadas a la derecha
            self._mover_a_layout(self.frame_pendientes, self._lay_col_izq)
            self._mover_a_layout(self.frame_completadas, self._lay_col_der)
            self.frame_pendientes.setVisible(True)
            self.frame_completadas.setVisible(True)

        elif modo == "pendientes":
            # Pendientes a la izquierda visible, Completadas a la derecha oculto
            self._mover_a_layout(self.frame_pendientes, self._lay_col_izq)
            self._mover_a_layout(self.frame_completadas, self._lay_col_der)
            self.frame_pendientes.setVisible(True)
            self.frame_completadas.setVisible(False)

        else:  # completadas
            # ✅ Completadas debe mostrarse en la izquierda
            self._mover_a_layout(self.frame_completadas, self._lay_col_izq)
            self._mover_a_layout(self.frame_pendientes, self._lay_col_der)
            self.frame_completadas.setVisible(True)
            self.frame_pendientes.setVisible(False)

    def _click_total(self) -> None:
        self.aplicar_modo_filtro("total")
        self.filtro_total_clicked.emit()

    def _click_pendientes(self) -> None:
        self.aplicar_modo_filtro("pendientes")
        self.filtro_pendientes_clicked.emit()

    def _click_completadas(self) -> None:
        self.aplicar_modo_filtro("completadas")
        self.filtro_completadas_clicked.emit()

    # -------------------- HU10: Ordenar (menu) --------------------

    def _crear_menu_ordenar(self) -> None:
        self._menu_ordenar = QMenu(self)

        self._menu_ordenar.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                padding: 6px;
            }
            QMenu::item {
                padding: 8px 14px;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: #e5e7eb;
            }
            QMenu::item:checked {
                font-weight: 700;
            }
        """)

        grupo = QActionGroup(self._menu_ordenar)
        grupo.setExclusive(True)

        self._act_orden_fecha = QAction("Por fecha", self._menu_ordenar)
        self._act_orden_fecha.setCheckable(True)
        self._act_orden_fecha.setChecked(True)

        self._act_orden_nombre = QAction("Por nombre", self._menu_ordenar)
        self._act_orden_nombre.setCheckable(True)

        grupo.addAction(self._act_orden_fecha)
        grupo.addAction(self._act_orden_nombre)

        self._menu_ordenar.addAction(self._act_orden_fecha)
        self._menu_ordenar.addAction(self._act_orden_nombre)

        self._act_orden_fecha.triggered.connect(lambda: self._set_orden("fecha"))
        self._act_orden_nombre.triggered.connect(lambda: self._set_orden("nombre"))

    def _mostrar_menu_ordenar(self) -> None:
        pos = self.btn_ordenar.mapToGlobal(self.btn_ordenar.rect().bottomLeft())
        self._menu_ordenar.exec(pos)

    def _set_orden(self, modo: str) -> None:
        modo = (modo or "fecha").strip().lower()
        if modo not in ("fecha", "nombre"):
            modo = "fecha"

        if self._modo_orden == modo:
            return

        self._modo_orden = modo
        self.ordenar_changed.emit(modo)

    # ------------------------------------------------------------------

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

        self.lbl_usuario = QLabel("Dashboard")
        self.lbl_usuario.setStyleSheet(
            "font-size: 20px; font-weight: 800; color: #ffffff;"
            "letter-spacing: -0.3px;"
        )
        topbar_layout.addWidget(self.lbl_usuario)

        topbar_layout.addStretch()

        # Centro: Registrar + Buscar + Ordenar ▾
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
        self.txt_buscar.setMinimumWidth(260)
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

        self.btn_ordenar = BotonAnimado(
            "Ordenar ▾",
            color_sombra="#111827",
            intensidad_sombra=55,
            blur_reposo=2.0,
            blur_hover=16.0,
        )
        self.btn_ordenar.setProperty("cssClass", "btn-ordenar")
        self.btn_ordenar.setFixedHeight(44)
        centro.addWidget(self.btn_ordenar)

        topbar_layout.addLayout(centro)
        topbar_layout.addStretch()

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

        contenido_layout.addSpacing(28)

        # ============ COLUMNAS (2 columnas siempre) ============
        columnas = QHBoxLayout()
        columnas.setSpacing(18)

        # Columna izquierda (contenedor)
        self.col_izq = QWidget()
        self._lay_col_izq = QVBoxLayout(self.col_izq)
        self._lay_col_izq.setContentsMargins(0, 0, 0, 0)
        self._lay_col_izq.setSpacing(0)

        # Columna derecha (contenedor)
        self.col_der = QWidget()
        self._lay_col_der = QVBoxLayout(self.col_der)
        self._lay_col_der.setContentsMargins(0, 0, 0, 0)
        self._lay_col_der.setSpacing(0)

        # --- Frame Pendientes ---
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

        # --- Frame Completadas ---
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

        # Estado inicial: Pendientes izq / Completadas der
        self._lay_col_izq.addWidget(self.frame_pendientes)
        self._lay_col_der.addWidget(self.frame_completadas)

        columnas.addWidget(self.col_izq, 1)
        columnas.addWidget(self.col_der, 1)
        columnas.setAlignment(self.col_izq, Qt.AlignmentFlag.AlignTop)
        columnas.setAlignment(self.col_der, Qt.AlignmentFlag.AlignTop)

        contenido_layout.addLayout(columnas)
        contenido_layout.addStretch()

        scroll.setWidget(contenido_widget)
        layout_raiz.addWidget(scroll, 1)

        # ============ CONEXIONES ============
        self.btn_registrar_tarea.clicked.connect(self.registrar_tarea_clicked.emit)
        self.btn_cerrar_sesion.clicked.connect(self.cerrar_sesion_clicked.emit)
        self.btn_buscar.clicked.connect(self._al_buscar)
        self.txt_buscar.returnPressed.connect(self._al_buscar)

        # HU08
        self.stat_total.clicked.connect(self._click_total)
        self.stat_pendientes.clicked.connect(self._click_pendientes)
        self.stat_completadas.clicked.connect(self._click_completadas)

        # HU10
        self._crear_menu_ordenar()
        self.btn_ordenar.clicked.connect(self._mostrar_menu_ordenar)

        # Estado inicial
        self.aplicar_modo_filtro("total")

    def _al_buscar(self):
        texto = self.txt_buscar.text().strip()
        self.buscar_clicked.emit(texto)

    def establecer_usuario(self, usuario: str):
        self._usuario = usuario
        self.lbl_subtitulo.setText(
            f"Bienvenido, {usuario}. Aqui tienes un resumen de tus tareas."
        )
        self.aplicar_modo_filtro("total")

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

        # Pendientes
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

        # Completadas
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