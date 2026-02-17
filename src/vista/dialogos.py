from __future__ import annotations

from PyQt6.QtWidgets import QMessageBox, QWidget


def mostrar_error(parent: QWidget, titulo: str, mensaje: str) -> None:
    """Muestra un diálogo de error."""
    QMessageBox.critical(parent, titulo, mensaje)


def mostrar_info(parent: QWidget, titulo: str, mensaje: str) -> None:
    """Muestra un diálogo informativo."""
    QMessageBox.information(parent, titulo, mensaje)


def confirmar(parent: QWidget, titulo: str, mensaje: str) -> bool:
    """Muestra un diálogo de confirmación (Sí/No)."""
    resp = QMessageBox.question(
        parent,
        titulo,
        mensaje,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    return resp == QMessageBox.StandardButton.Yes
