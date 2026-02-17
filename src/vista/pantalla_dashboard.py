from __future__ import annotations

from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.vista.controlador_tareas_vista import ControladorTareas, TareaVista, UsuarioSesion
from src.vista.dialogos import confirmar, mostrar_error, mostrar_info
from src.vista.widgets.formulario_tarea import DatosFormularioTarea, FormularioTarea
from src.vista.widgets.tarjeta_tarea import TarjetaTarea


class FiltroTareas(str, Enum):
    TODAS = "todas"
    PENDIENTES = "pendientes"
    COMPLETADAS = "completadas"


class PantallaDashboard(QWidget):
    """Dashboard con listado + formulario lateral y modo pantalla completa."""

    def __init__(
        self,
        sesion: UsuarioSesion,
        controlador: ControladorTareas,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("DashboardRoot")

        self._sesion = sesion
        self._controlador = controlador

        self._filtro = FiltroTareas.TODAS
        self._texto_busqueda = ""

        self._btn_chip_todas = QPushButton("Todas")
        self._btn_chip_pend = QPushButton("Pendientes")
        self._btn_chip_comp = QPushButton("Completadas")

        for btn in (self._btn_chip_todas, self._btn_chip_pend, self._btn_chip_comp):
            btn.setObjectName("Chip")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self._btn_chip_todas.clicked.connect(lambda: self._set_filtro(FiltroTareas.TODAS))
        self._btn_chip_pend.clicked.connect(
            lambda: self._set_filtro(FiltroTareas.PENDIENTES)
        )
        self._btn_chip_comp.clicked.connect(
            lambda: self._set_filtro(FiltroTareas.COMPLETADAS)
        )

        self._buscar = QLineEdit()
        self._buscar.setObjectName("BuscarInput")
        self._buscar.setPlaceholderText("Buscar por título…")
        self._buscar.textChanged.connect(self._on_buscar)

        self._btn_nueva = QPushButton("Nueva tarea")
        self._btn_nueva.setObjectName("BtnPrimario")
        self._btn_nueva.clicked.connect(self._nueva_tarea)

        self._btn_full = QPushButton("Formulario pantalla completa")
        self._btn_full.setObjectName("BtnSecundario")
        self._btn_full.clicked.connect(self._abrir_formulario_fullscreen)

        top_bar = self._crear_topbar()

        # Listado (scroll + tarjetas)
        self._panel_lista = QFrame()
        self._panel_lista.setObjectName("PanelLista")
        lista_layout = QVBoxLayout(self._panel_lista)
        lista_layout.setContentsMargins(16, 16, 16, 16)
        lista_layout.setSpacing(12)

        self._lbl_subtitulo = QLabel("Tus tareas")
        self._lbl_subtitulo.setObjectName("MetaTarea")

        self._contenedor_tarjetas = QWidget()
        self._contenedor_layout = QVBoxLayout(self._contenedor_tarjetas)
        self._contenedor_layout.setContentsMargins(0, 0, 0, 0)
        self._contenedor_layout.setSpacing(10)
        self._contenedor_layout.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(self._contenedor_tarjetas)

        lista_layout.addWidget(self._lbl_subtitulo)
        lista_layout.addWidget(scroll)

        # Formulario lateral
        self._formulario = FormularioTarea()
        self._formulario.guardar.connect(self._guardar_formulario)
        self._formulario.cancelar.connect(self._cancelar_formulario)

        # Splitter (lista + formulario lateral)
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.addWidget(self._panel_lista)
        splitter.addWidget(self._formulario)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        # Vista normal (splitter)
        vista_split = QWidget()
        vs_layout = QVBoxLayout(vista_split)
        vs_layout.setContentsMargins(0, 0, 0, 0)
        vs_layout.addWidget(splitter)

        # Vista fullscreen del formulario
        self._formulario_full = FormularioTarea()
        self._formulario_full.guardar.connect(self._guardar_formulario_full)
        self._formulario_full.cancelar.connect(self._volver_desde_fullscreen)

        self._btn_volver = QPushButton("← Volver al listado")
        self._btn_volver.setObjectName("BtnSecundario")
        self._btn_volver.clicked.connect(self._volver_desde_fullscreen)

        vista_full = QWidget()
        vf_layout = QVBoxLayout(vista_full)
        vf_layout.setContentsMargins(0, 0, 0, 0)
        vf_layout.setSpacing(10)

        vf_layout.addWidget(self._btn_volver, alignment=Qt.AlignmentFlag.AlignLeft)
        vf_layout.addWidget(self._formulario_full)

        self._stack_cuerpo = QStackedWidget()
        self._stack_cuerpo.addWidget(vista_split)  # index 0
        self._stack_cuerpo.addWidget(vista_full)  # index 1

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)
        root.addWidget(top_bar)
        root.addWidget(self._stack_cuerpo)

        self._refrescar_chips()
        self._refrescar_listado()

    def _crear_topbar(self) -> QFrame:
        top = QFrame()
        top.setObjectName("TopBar")

        titulo = QLabel("Dashboard de Tareas")
        titulo.setObjectName("AppTitle")

        usuario = QLabel(f"Usuario: {self._sesion.username}")
        usuario.setObjectName("MetaTarea")

        chips = QHBoxLayout()
        chips.setSpacing(8)
        chips.addWidget(self._btn_chip_todas)
        chips.addWidget(self._btn_chip_pend)
        chips.addWidget(self._btn_chip_comp)
        chips.addStretch(1)

        fila_sup = QHBoxLayout()
        fila_sup.addWidget(titulo)
        fila_sup.addStretch(1)
        fila_sup.addWidget(usuario)

        fila_inf = QHBoxLayout()
        fila_inf.setSpacing(10)
        fila_inf.addLayout(chips)
        fila_inf.addWidget(self._buscar, stretch=2)
        fila_inf.addWidget(self._btn_full)
        fila_inf.addWidget(self._btn_nueva)

        layout = QVBoxLayout(top)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)
        layout.addLayout(fila_sup)
        layout.addLayout(fila_inf)

        return top

    def _set_filtro(self, filtro: FiltroTareas) -> None:
        self._filtro = filtro
        self._refrescar_chips()
        self._refrescar_listado()

    def _refrescar_chips(self) -> None:
        self._btn_chip_todas.setObjectName("Chip")
        self._btn_chip_pend.setObjectName("Chip")
        self._btn_chip_comp.setObjectName("Chip")

        if self._filtro == FiltroTareas.TODAS:
            self._btn_chip_todas.setObjectName("ChipActivo")
        elif self._filtro == FiltroTareas.PENDIENTES:
            self._btn_chip_pend.setObjectName("ChipActivo")
        elif self._filtro == FiltroTareas.COMPLETADAS:
            self._btn_chip_comp.setObjectName("ChipActivo")

        # Fuerza re-aplicar estilo (cuando cambia objectName)
        for btn in (self._btn_chip_todas, self._btn_chip_pend, self._btn_chip_comp):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_buscar(self, texto: str) -> None:
        self._texto_busqueda = (texto or "").strip().lower()
        self._refrescar_listado()

    def _obtener_tareas_filtradas(self) -> list[TareaVista]:
        tareas = self._controlador.listar(self._sesion.id_usuario)

        if self._filtro == FiltroTareas.PENDIENTES:
            tareas = [t for t in tareas if not t.completada]
        elif self._filtro == FiltroTareas.COMPLETADAS:
            tareas = [t for t in tareas if t.completada]

        if self._texto_busqueda:
            tareas = [t for t in tareas if self._texto_busqueda in t.titulo.lower()]

        tareas.sort(key=lambda t: t.creada_en, reverse=True)
        return tareas

    def _limpiar_tarjetas(self) -> None:
        while self._contenedor_layout.count() > 0:
            item = self._contenedor_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self._contenedor_layout.addStretch(1)

    def _refrescar_listado(self) -> None:
        self._limpiar_tarjetas()
        tareas = self._obtener_tareas_filtradas()

        if not tareas:
            vacio = QLabel("No hay tareas para mostrar con los filtros actuales.")
            vacio.setObjectName("MetaTarea")
            self._contenedor_layout.insertWidget(0, vacio)
            return

        for tarea in tareas:
            card = TarjetaTarea(tarea)
            card.editar.connect(self._editar_tarea)
            card.eliminar.connect(self._eliminar_tarea)
            card.alternar_completada.connect(self._alternar_completada)
            self._contenedor_layout.insertWidget(self._contenedor_layout.count() - 1, card)

    def _nueva_tarea(self) -> None:
        self._formulario.modo_crear()
        self._stack_cuerpo.setCurrentIndex(0)

    def _editar_tarea(self, id_tarea: int) -> None:
        tarea = self._buscar_tarea_por_id(id_tarea)
        if tarea is None:
            mostrar_error(self, "Error", "La tarea no existe.")
            return
        self._formulario.modo_editar(tarea)
        self._stack_cuerpo.setCurrentIndex(0)

    def _buscar_tarea_por_id(self, id_tarea: int) -> TareaVista | None:
        tareas = self._controlador.listar(self._sesion.id_usuario)
        for t in tareas:
            if t.id_tarea == id_tarea:
                return t
        return None

    def _guardar_formulario(self, datos: DatosFormularioTarea) -> None:
        self._guardar(datos, modo_full=False)

    def _guardar_formulario_full(self, datos: DatosFormularioTarea) -> None:
        self._guardar(datos, modo_full=True)

    def _guardar(self, datos: DatosFormularioTarea, *, modo_full: bool) -> None:
        titulo = (datos.titulo or "").strip()
        if not titulo:
            mostrar_error(self, "Validación", "El título no puede estar vacío.")
            return

        formulario = self._formulario_full if modo_full else self._formulario
        id_tarea = formulario.id_tarea

        if id_tarea is None:
            nueva = self._controlador.crear(
                self._sesion.id_usuario, titulo, datos.descripcion
            )
            if nueva is None:
                mostrar_error(
                    self,
                    "Validación",
                    "No se pudo crear. Puede ser título vacío o duplicado.",
                )
                return
            if datos.completada:
                self._controlador.marcar_completada(
                    self._sesion.id_usuario, nueva.id_tarea, True
                )
            mostrar_info(self, "OK", "Tarea creada correctamente.")
            formulario.modo_crear()
        else:
            ok = self._controlador.editar(
                self._sesion.id_usuario,
                id_tarea,
                titulo,
                datos.descripcion,
            )
            if not ok:
                mostrar_error(
                    self,
                    "Validación",
                    "No se pudo editar. Puede ser título vacío o duplicado.",
                )
                return
            self._controlador.marcar_completada(
                self._sesion.id_usuario, id_tarea, datos.completada
            )
            mostrar_info(self, "OK", "Tarea actualizada correctamente.")
            formulario.modo_crear()

        self._refrescar_listado()

        if modo_full:
            self._volver_desde_fullscreen()

    def _cancelar_formulario(self) -> None:
        self._formulario.modo_crear()

    def _eliminar_tarea(self, id_tarea: int) -> None:
        if not confirmar(self, "Confirmación", "¿Deseas eliminar esta tarea?"):
            return

        ok = self._controlador.eliminar(self._sesion.id_usuario, id_tarea)
        if not ok:
            mostrar_error(self, "Error", "No se pudo eliminar (no existe).")
            return

        self._refrescar_listado()

    def _alternar_completada(self, id_tarea: int, completada: bool) -> None:
        ok = self._controlador.marcar_completada(
            self._sesion.id_usuario, id_tarea, completada
        )
        if not ok:
            mostrar_error(self, "Error", "No se pudo actualizar el estado.")
            return
        self._refrescar_listado()

    def _abrir_formulario_fullscreen(self) -> None:
        # Copia estado del formulario lateral al fullscreen
        tarea_id = self._formulario.id_tarea
        if tarea_id is None:
            self._formulario_full.modo_crear()
        else:
            tarea = self._buscar_tarea_por_id(tarea_id)
            if tarea is not None:
                self._formulario_full.modo_editar(tarea)
            else:
                self._formulario_full.modo_crear()

        self._stack_cuerpo.setCurrentIndex(1)

    def _volver_desde_fullscreen(self) -> None:
        self._formulario_full.modo_crear()
        self._stack_cuerpo.setCurrentIndex(0)
