# main.py
from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from src.vista.controlador_tareas_vista import cargar_estilos_qss
from src.vista.ventana_principal import VentanaPrincipal


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(cargar_estilos_qss())

    ventana = VentanaPrincipal()
    ventana.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
