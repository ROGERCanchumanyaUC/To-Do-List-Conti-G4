# src/vista/pantalla_dashboard.py
from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.vista.controlador_tareas_vista import ControladorTareasVista, SesionVista, TareaVista


class PantallaDashboard(QWidget):
    logout_solicitado = pyqtSignal()
    registrar_tarea_solicitada = pyqtSignal()
    editar_tarea_solicitada = pyqtSignal(str)

    def __init__(self, *, sesion: SesionVista, controlador: ControladorTareasVista) -> None:
        super().__init__()
        self.setObjectName("DashboardRoot")

        self._sesion = sesion
        self._controlador = controlador

        self._lbl_contador = QLabel("")
        self._input_buscar = QLineEdit()
        self._chips: dict[str, QPushButton] = {}

        self._lbl_total = QLabel("0")
        self._lbl_pendientes = QLabel("0")
        self._lbl_completadas = QLabel("0")

        self._btn_logout = QPushButton("Cerrar Sesión")
        self._btn_registrar = QPushButton("Registrar Tarea")

        self._scroll = QScrollArea()
        self._contenedor_listas = QWidget()
        self._layout_listas = QVBoxLayout(self._contenedor_listas)

        self._construir_ui()
        self._conectar_eventos()
        self._refrescar_ui()

        if self._controlador.mostrar_tutorial:
            self._mostrar_tutorial()

    def _construir_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = QFrame()
        header.setObjectName("Header")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 18, 24, 18)

        box_tit = QVBoxLayout()
        lbl_tit = QLabel("Mis Tareas")
        lbl_tit.setObjectName("HeaderTitulo")
        lbl_user = QLabel(self._sesion.username)
        lbl_user.setObjectName("HeaderUsuario")
        box_tit.addWidget(lbl_tit)
        box_tit.addWidget(lbl_user)

        self._btn_logout.setObjectName("BotonLogout")

        header_layout.addLayout(box_tit)
        header_layout.addStretch(1)
        header_layout.addWidget(self._btn_logout)

        root.addWidget(header)

        # Contenido
        cont = QWidget()
        cont_layout = QVBoxLayout(cont)
        cont_layout.setContentsMargins(24, 24, 24, 24)
        cont_layout.setSpacing(16)

        # Panel búsqueda/filtros + acción registrar
        panel = QFrame()
        panel.setObjectName("PanelBlanco")
        p_layout = QVBoxLayout(panel)
        p_layout.setContentsMargins(18, 18, 18, 18)
        p_layout.setSpacing(12)

        row_top = QHBoxLayout()
        lbl_buscar = QLabel("Buscar tareas")
        lbl_buscar.setObjectName("Subtitulo")

        self._btn_registrar.setObjectName("BotonPrimario")
        self._btn_registrar.setText("Registrar Tarea")

        row_top.addWidget(lbl_buscar)
        row_top.addStretch(1)
        row_top.addWidget(self._btn_registrar)

        self._input_buscar.setPlaceholderText("Buscar por nombre de la tarea...")

        p_layout.addLayout(row_top)
        p_layout.addWidget(self._input_buscar)

        lbl_filtro = QLabel("Filtrar por categoría")
        lbl_filtro.setObjectName("Subtitulo")
        p_layout.addWidget(lbl_filtro)

        row_chips = QHBoxLayout()
        row_chips.setSpacing(10)

        for key, text in [
            ("todas", "Todas las tareas"),
            ("no importante", "No importante"),
            ("obligatorio", "Obligatorio"),
            ("pendiente", "Pendiente"),
            ("completadas", "Completadas"),
        ]:
            btn = QPushButton(text)
            btn.setObjectName("Chip")
            btn.setProperty("activo", "false")
            self._chips[key] = btn
            row_chips.addWidget(btn)

        row_chips.addStretch(1)
        p_layout.addLayout(row_chips)

        p_layout.addWidget(self._lbl_contador)

        cont_layout.addWidget(panel)

        # Estadísticas
        stats = QGridLayout()
        stats.setHorizontalSpacing(12)
        stats.setVerticalSpacing(12)

        stats.addWidget(self._crear_card_estadistica("Total de Tareas", self._lbl_total), 0, 0)
        stats.addWidget(self._crear_card_estadistica("Tareas Pendientes", self._lbl_pendientes), 0, 1)
        stats.addWidget(self._crear_card_estadistica("Tareas Completadas", self._lbl_completadas), 0, 2)

        cont_layout.addLayout(stats)

        # Listas
        self._scroll.setWidgetResizable(True)
        self._layout_listas.setContentsMargins(0, 0, 0, 0)
        self._layout_listas.setSpacing(12)
        self._scroll.setWidget(self._contenedor_listas)

        cont_layout.addWidget(self._scroll, 1)

        root.addWidget(cont, 1)

    def _crear_card_estadistica(self, titulo: str, lbl_valor: QLabel) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)

        lbl_t = QLabel(titulo)
        lbl_t.setObjectName("TextoPequeno")

        lbl_valor.setText("0")
        lbl_valor.setStyleSheet("font-size: 28px; font-weight: 800; color: #111827;")

        layout.addWidget(lbl_t)
        layout.addWidget(lbl_valor)
        return card

    def _conectar_eventos(self) -> None:
        self._btn_logout.clicked.connect(self.logout_solicitado.emit)
        self._btn_registrar.clicked.connect(self.registrar_tarea_solicitada.emit)

        self._input_buscar.textChanged.connect(self._controlador.set_search_query)

        for key, btn in self._chips.items():
            btn.clicked.connect(lambda _=False, k=key: self._controlador.set_category_filter(k))

        self._controlador.datos_cambiaron.connect(self._refrescar_ui)

    def _mostrar_tutorial(self) -> None:
        msg = (
            "Guía rápida:\n\n"
            "1) Usa Buscar para filtrar por nombre.\n"
            "2) Usa los filtros por categoría.\n"
            "3) Presiona 'Registrar Tarea' para crear una nueva.\n"
            "4) Edita desde cada tarjeta.\n"
        )
        QMessageBox.information(self, "Tutorial", msg)
        self._controlador.cerrar_tutorial()

    def _refrescar_ui(self) -> None:
        filtro = getattr(self._controlador, "_category_filter", "todas")  # noqa: SLF001
        for k, btn in self._chips.items():
            btn.setProperty("activo", "true" if k == filtro else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        tareas_filtradas = self._controlador.tareas_filtradas()
        tareas_total = self._controlador.tareas

        pendientes = [t for t in tareas_filtradas if not t.completed]
        completadas = [t for t in tareas_filtradas if t.completed]

        self._lbl_total.setText(str(len(tareas_total)))
        self._lbl_pendientes.setText(str(len([t for t in tareas_total if not t.completed])))
        self._lbl_completadas.setText(str(len([t for t in tareas_total if t.completed])))

        if self._controlador._search_query or filtro != "todas":  # noqa: SLF001
            self._lbl_contador.setText(
                f"Mostrando {len(tareas_filtradas)} de {len(tareas_total)} tareas"
            )
        else:
            self._lbl_contador.setText("")

        while self._layout_listas.count():
            item = self._layout_listas.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        if filtro == "todas" or filtro != "completadas":
            self._layout_listas.addWidget(self._crear_seccion("Tareas Pendientes", pendientes, es_completadas=False))

        if (filtro == "todas" or filtro == "completadas") and completadas:
            self._layout_listas.addWidget(self._crear_seccion("Tareas Completadas", completadas, es_completadas=True))

        self._layout_listas.addStretch(1)

    def _crear_seccion(self, titulo: str, tareas: list[TareaVista], *, es_completadas: bool) -> QFrame:
        box = QFrame()
        box.setObjectName("PanelBlanco")
        layout = QVBoxLayout(box)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        lbl = QLabel(titulo)
        lbl.setStyleSheet("font-size: 20px; font-weight: 800; color: #111827;")
        layout.addWidget(lbl)

        if not tareas:
            texto = (
                "No se encontraron tareas que coincidan con los filtros"
                if (self._controlador._search_query or self._controlador._category_filter != "todas")  # noqa: SLF001
                else ("No tienes tareas completadas" if es_completadas else "No tienes tareas pendientes")
            )
            subt = (
                "Intenta con otros criterios de búsqueda"
                if (self._controlador._search_query or self._controlador._category_filter != "todas")  # noqa: SLF001
                else "¡Agrega una nueva tarea para comenzar!"
            )
            empty = QLabel(f"{texto}\n{subt}")
            empty.setObjectName("TextoPequeno")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("padding: 18px;")
            layout.addWidget(empty)
            return box

        for t in tareas:
            layout.addWidget(self._crear_card_tarea(t))

        return box

    def _crear_card_tarea(self, tarea: TareaVista) -> QFrame:
        card = QFrame()
        card.setObjectName("TaskCard")

        l = QHBoxLayout(card)
        l.setContentsMargins(14, 14, 14, 14)
        l.setSpacing(12)

        btn_check = QPushButton("✓" if tarea.completed else "")
        btn_check.setFixedSize(28, 28)
        btn_check.setStyleSheet(
            "border-radius: 14px; border: 2px solid #9ca3af; font-weight: 900;"
            + ("background:#dcfce7; border-color:#16a34a; color:#16a34a;" if tarea.completed else "")
        )
        btn_check.clicked.connect(lambda _=False, tid=tarea.id: self._controlador.alternar_completada(tid))

        centro = QVBoxLayout()
        centro.setSpacing(6)

        row_top = QHBoxLayout()
        titulo = QLabel(tarea.name)
        titulo.setStyleSheet(
            "font-size: 16px; font-weight: 800; color: #111827;"
            + (" text-decoration: line-through; color:#6b7280;" if tarea.completed else "")
        )

        fecha = QLabel(self._format_date(tarea.created_at))
        fecha.setObjectName("TextoPequeno")
        row_top.addWidget(titulo)
        row_top.addStretch(1)
        row_top.addWidget(fecha)

        detalle = QLabel(tarea.detail)
        detalle.setWordWrap(True)
        detalle.setStyleSheet(
            "color:#4b5563;"
            + (" text-decoration: line-through; color:#6b7280;" if tarea.completed else "")
        )

        centro.addLayout(row_top)
        centro.addWidget(detalle)

        acciones = QVBoxLayout()
        acciones.setSpacing(8)

        btn_editar = QPushButton("Editar")
        btn_editar.setObjectName("LinkNaranja")
        btn_editar.clicked.connect(lambda _=False, tid=tarea.id: self.editar_tarea_solicitada.emit(tid))

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("LinkRojo")
        btn_eliminar.clicked.connect(lambda _=False, tid=tarea.id: self._confirmar_eliminar(tid))

        acciones.addWidget(btn_editar)
        acciones.addWidget(btn_eliminar)
        acciones.addStretch(1)

        l.addWidget(btn_check, 0, Qt.AlignmentFlag.AlignTop)
        l.addLayout(centro, 1)
        l.addLayout(acciones)

        return card

    def _confirmar_eliminar(self, task_id: str) -> None:
        r = QMessageBox.question(
            self,
            "Confirmación",
            "¿Estás seguro de eliminar esta tarea?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if r == QMessageBox.StandardButton.Yes:
            self._controlador.eliminar_tarea(task_id)

    def _format_date(self, date: datetime) -> str:
        now = datetime.now()
        diff_days = abs((now.date() - date.date()).days)

        if diff_days == 0:
            return "Hoy"
        if diff_days == 1:
            return "Ayer"
        if diff_days < 7:
            return f"Hace {diff_days} días"
        return date.strftime("%d %b %Y")
