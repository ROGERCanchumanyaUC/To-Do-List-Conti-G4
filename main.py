from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.vista.ventana_principal import VentanaPrincipal


def cargar_qss(app: QApplication) -> None:
    """Carga el archivo de estilos QSS de la vista."""
    ruta_qss = Path(__file__).resolve().parent / "src" / "vista" / "estilos.qss"
    if ruta_qss.exists():
        app.setStyleSheet(ruta_qss.read_text(encoding="utf-8"))


def main() -> int:
    """Punto de entrada del aplicativo (solo vista)."""
    app = QApplication(sys.argv)
    app.setApplicationName("OPPRA")

    cargar_qss(app)

    ventana = VentanaPrincipal()
    ventana.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
