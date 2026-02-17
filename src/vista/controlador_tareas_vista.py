# src/vista/controlador_tareas_vista.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal


@dataclass(frozen=True)
class SesionVista:
    """Datos mínimos de sesión para la capa vista."""
    username: str


@dataclass
class TareaVista:
    """Modelo temporal para la vista (luego se conectará con la BD/lógica)."""
    id: str
    name: str
    category: str
    time_value: int
    time_unit: str
    detail: str
    completed: bool
    created_at: datetime


def cargar_estilos_qss() -> str:
    """
    Carga estilos desde src/vista/estilos.qss si existe.
    Si no existe, usa un QSS base integrado.
    """
    ruta_qss = Path(__file__).with_name("estilos.qss")
    if ruta_qss.exists():
        return ruta_qss.read_text(encoding="utf-8")

    # Fallback (estilo base)
    return """
    QWidget { font-family: "Segoe UI"; font-size: 14px; }
    QWidget#LoginRoot, QWidget#DashboardRoot {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #eff6ff, stop:1 #f5f3ff);
    }

    QFrame#LoginCard, QFrame#PanelBlanco, QFrame#Card {
        background: #ffffff;
        border: 1px solid rgba(0,0,0,0.10);
        border-radius: 14px;
    }

    QLabel#TituloGrande { font-size: 26px; font-weight: 700; color: #111827; }
    QLabel#Subtitulo { color: #6b7280; }
    QLabel#TextoPequeno { color: #6b7280; }

    QLineEdit, QTextEdit, QSpinBox, QComboBox {
        background: #f3f3f5;
        border: 2px solid #d1d5db;
        border-radius: 10px;
        padding: 10px;
        color: #111827;
    }
    QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
        border: 2px solid #2563eb;
        outline: none;
    }

    QPushButton#BotonPrimario {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #2563eb, stop:1 #7c3aed);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
    }
    QPushButton#BotonPrimario:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #1d4ed8, stop:1 #6d28d9);
    }

    QPushButton#BotonSecundario {
        background: #e5e7eb;
        color: #111827;
        border: none;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
    }
    QPushButton#BotonSecundario:hover { background: #d1d5db; }

    QFrame#Header {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #2563eb, stop:1 #7c3aed);
        border: none;
    }
    QLabel#HeaderTitulo { color: white; font-size: 24px; font-weight: 800; }
    QLabel#HeaderUsuario { color: rgba(255,255,255,0.85); }

    QPushButton#BotonLogout {
        background: #ffffff;
        color: #2563eb;
        border: none;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 800;
    }
    QPushButton#BotonLogout:hover { background: #eff6ff; }

    QPushButton#Chip {
        background: #f3f4f6;
        color: #111827;
        border: none;
        border-radius: 12px;
        padding: 8px 12px;
        font-weight: 700;
    }
    QPushButton#Chip[activo="true"] {
        background: #2563eb;
        color: white;
    }

    QFrame#TaskCard {
        background: #ffffff;
        border: 2px solid #e5e7eb;
        border-radius: 14px;
    }
    QFrame#TaskCard:hover { border: 2px solid #c7d2fe; }

    QPushButton#LinkNaranja {
        color: #f97316;
        background: transparent;
        border: none;
        font-weight: 700;
        text-align: left;
    }
    QPushButton#LinkNaranja:hover { background: #fff7ed; border-radius: 10px; padding: 8px; }

    QPushButton#LinkRojo {
        color: #ef4444;
        background: transparent;
        border: none;
        font-weight: 700;
        text-align: left;
    }
    QPushButton#LinkRojo:hover { background: #fef2f2; border-radius: 10px; padding: 8px; }

    QLabel#Badge {
        border-radius: 999px;
        padding: 4px 10px;
        font-weight: 700;
    }
    QLabel#BadgeAzul { background: #dbeafe; color: #1d4ed8; border: 1px solid #93c5fd; }
    QLabel#BadgeRojo { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
    QLabel#BadgeAmarillo { background: #fef9c3; color: #a16207; border: 1px solid #fde68a; }
    QLabel#BadgeGris { background: #f3f4f6; color: #374151; border: 1px solid #d1d5db; }
    QLabel#BadgeVerde { background: #dcfce7; color: #166534; border: 1px solid #86efac; }
    """


class ControladorTareasVista(QObject):
    """
    Controlador de estado para la vista (sin BD por ahora).
    Luego se conectará con la lógica real.
    """

    datos_cambiaron = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._tareas: list[TareaVista] = []
        self._search_query: str = ""
        self._category_filter: str = "todas"
        self._mostrar_tutorial: bool = True

    # -------------------
    # Estado UI
    # -------------------
    @property
    def mostrar_tutorial(self) -> bool:
        return self._mostrar_tutorial

    def cerrar_tutorial(self) -> None:
        self._mostrar_tutorial = False
        self.datos_cambiaron.emit()

    @property
    def tareas(self) -> list[TareaVista]:
        return list(self._tareas)

    def set_search_query(self, texto: str) -> None:
        self._search_query = (texto or "").strip()
        self.datos_cambiaron.emit()

    def set_category_filter(self, filtro: str) -> None:
        self._category_filter = filtro
        self.datos_cambiaron.emit()

    # -------------------
    # CRUD (vista)
    # -------------------
    def agregar_tarea(
        self,
        *,
        name: str,
        category: str,
        time_value: int,
        time_unit: str,
        detail: str,
    ) -> None:
        tarea = TareaVista(
            id=str(int(datetime.now().timestamp() * 1000)),
            name=name,
            category=category,
            time_value=int(time_value),
            time_unit=time_unit,
            detail=detail,
            completed=False,
            created_at=datetime.now(),
        )
        self._tareas.append(tarea)
        self.datos_cambiaron.emit()

    def editar_tarea(
        self,
        task_id: str,
        *,
        name: str,
        category: str,
        time_value: int,
        time_unit: str,
        detail: str,
    ) -> None:
        for t in self._tareas:
            if t.id == task_id:
                t.name = name
                t.category = category
                t.time_value = int(time_value)
                t.time_unit = time_unit
                t.detail = detail
                break
        self.datos_cambiaron.emit()

    def alternar_completada(self, task_id: str) -> None:
        for t in self._tareas:
            if t.id == task_id:
                t.completed = not t.completed
                break
        self.datos_cambiaron.emit()

    def eliminar_tarea(self, task_id: str) -> None:
        self._tareas = [t for t in self._tareas if t.id != task_id]
        self.datos_cambiaron.emit()

    # -------------------
    # Filtros
    # -------------------
    def tareas_filtradas(self) -> list[TareaVista]:
        tareas = self._tareas

        if self._search_query:
            q = self._search_query.lower()
            tareas = [t for t in tareas if q in t.name.lower()]

        if self._category_filter == "completadas":
            tareas = [t for t in tareas if t.completed]
        elif self._category_filter == "todas":
            pass
        else:
            tareas = [t for t in tareas if (not t.completed and t.category == self._category_filter)]

        return list(tareas)
