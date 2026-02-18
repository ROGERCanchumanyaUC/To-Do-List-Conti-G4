"""
Punto de entrada de la aplicacion Todo App.
Crea la aplicacion PyQt6, carga estilos QSS y muestra la ventana principal.
"""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from src.modelo.conexion import init_db
from src.vista.ventana_principal import VentanaPrincipal


def cargar_estilos(app: QApplication) -> None:
    """Carga la hoja de estilos QSS desde el archivo."""
    ruta_estilos = Path(__file__).parent / "src" / "vista" / "estilos.qss"

    if ruta_estilos.exists():
        with open(ruta_estilos, "r", encoding="utf-8") as archivo:
            app.setStyleSheet(archivo.read())
        print(f"[OK] Estilos cargados desde: {ruta_estilos}")
    else:
        print(f"[AVISO] No se encontro archivo de estilos: {ruta_estilos}")


def main():
    """Funcion principal que inicia la aplicacion."""
    init_db()

    app = QApplication(sys.argv)
    app.setApplicationName("Todo App")
    app.setApplicationDisplayName("Todo App - Gestor de Tareas")

    fuente = QFont("Segoe UI", 10)
    fuente.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(fuente)

    cargar_estilos(app)

    ventana = VentanaPrincipal()
    ventana.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
