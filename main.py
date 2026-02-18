"""
Punto de entrada de la aplicacion Todo App.
Crea la aplicacion PyQt6, carga estilos QSS y muestra la ventana principal.
"""

import sys
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.vista.ventana_principal import VentanaPrincipal


def cargar_estilos(app: QApplication) -> None:
    """Carga la hoja de estilos QSS desde el archivo."""
    ruta_estilos = (
        Path(__file__).parent / "src" / "vista" / "estilos.qss"
    )

    if ruta_estilos.exists():
        with open(ruta_estilos, "r", encoding="utf-8") as archivo:
            app.setStyleSheet(archivo.read())
        print(f"[OK] Estilos cargados desde: {ruta_estilos}")
    else:
        print(f"[AVISO] No se encontro archivo de estilos: {ruta_estilos}")


def main():
    """Funcion principal que inicia la aplicacion."""
    app = QApplication(sys.argv)
    app.setApplicationName("Todo App")
    app.setApplicationDisplayName("Todo App - Gestor de Tareas")

    # Cargar estilos QSS
    cargar_estilos(app)

    # Crear y mostrar la ventana principal a pantalla completa
    ventana = VentanaPrincipal()
    ventana.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
