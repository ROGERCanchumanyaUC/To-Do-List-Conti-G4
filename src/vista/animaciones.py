"""
Widgets animados reutilizables para la aplicacion.
Incluye botones con animacion de sombra al hover y tarjetas animadas.
"""

from PyQt6.QtWidgets import (
    QPushButton,
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QParallelAnimationGroup,
    QPointF,
    Qt,
)
from PyQt6.QtGui import QColor


class BotonAnimado(QPushButton):
    """
    Boton con animacion suave de sombra al pasar el mouse.
    La sombra se eleva y se intensifica en hover, dando efecto de 'lift'.
    El color de la sombra se puede personalizar para que combine con el boton.
    """

    def __init__(
        self,
        texto: str = "",
        color_sombra: str = "#000000",
        intensidad_sombra: int = 50,
        blur_reposo: float = 0.0,
        blur_hover: float = 18.0,
        offset_reposo: QPointF = None,
        offset_hover: QPointF = None,
        duracion: int = 200,
        parent=None,
    ):
        super().__init__(texto, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        if offset_reposo is None:
            offset_reposo = QPointF(0, 1)
        if offset_hover is None:
            offset_hover = QPointF(0, 6)

        self._blur_reposo = blur_reposo
        self._blur_hover = blur_hover
        self._offset_reposo = offset_reposo
        self._offset_hover = offset_hover
        self._duracion = duracion

        # Crear efecto de sombra
        self._sombra = QGraphicsDropShadowEffect(self)
        self._sombra.setBlurRadius(blur_reposo)
        self._sombra.setOffset(offset_reposo)

        c = QColor(color_sombra)
        c.setAlpha(intensidad_sombra)
        self._sombra.setColor(c)
        self.setGraphicsEffect(self._sombra)

        # Animacion de blur
        self._anim_blur = QPropertyAnimation(self._sombra, b"blurRadius")
        self._anim_blur.setDuration(duracion)
        self._anim_blur.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Animacion de offset
        self._anim_offset = QPropertyAnimation(self._sombra, b"offset")
        self._anim_offset.setDuration(duracion)
        self._anim_offset.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Grupo paralelo
        self._grupo_hover = QParallelAnimationGroup(self)
        self._grupo_hover.addAnimation(self._anim_blur)
        self._grupo_hover.addAnimation(self._anim_offset)

    def enterEvent(self, event):
        self._grupo_hover.stop()
        self._anim_blur.setStartValue(self._sombra.blurRadius())
        self._anim_blur.setEndValue(self._blur_hover)
        self._anim_offset.setStartValue(self._sombra.offset())
        self._anim_offset.setEndValue(self._offset_hover)
        self._grupo_hover.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._grupo_hover.stop()
        self._anim_blur.setStartValue(self._sombra.blurRadius())
        self._anim_blur.setEndValue(self._blur_reposo)
        self._anim_offset.setStartValue(self._sombra.offset())
        self._anim_offset.setEndValue(self._offset_reposo)
        self._grupo_hover.start()
        super().leaveEvent(event)


class TarjetaAnimada(QFrame):
    """
    Frame/card con animacion de sombra al hover.
    Efecto: la tarjeta 'se eleva' cuando el mouse pasa por encima.
    """

    def __init__(
        self,
        color_sombra: str = "#000000",
        intensidad: int = 20,
        blur_reposo: float = 8.0,
        blur_hover: float = 28.0,
        duracion: int = 250,
        parent=None,
    ):
        super().__init__(parent)

        self._blur_reposo = blur_reposo
        self._blur_hover = blur_hover

        self._sombra = QGraphicsDropShadowEffect(self)
        self._sombra.setBlurRadius(blur_reposo)
        self._sombra.setOffset(QPointF(0, 2))

        c = QColor(color_sombra)
        c.setAlpha(intensidad)
        self._sombra.setColor(c)
        self.setGraphicsEffect(self._sombra)

        self._anim_blur = QPropertyAnimation(self._sombra, b"blurRadius")
        self._anim_blur.setDuration(duracion)
        self._anim_blur.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._anim_offset = QPropertyAnimation(self._sombra, b"offset")
        self._anim_offset.setDuration(duracion)
        self._anim_offset.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._grupo = QParallelAnimationGroup(self)
        self._grupo.addAnimation(self._anim_blur)
        self._grupo.addAnimation(self._anim_offset)

    def enterEvent(self, event):
        self._grupo.stop()
        self._anim_blur.setStartValue(self._sombra.blurRadius())
        self._anim_blur.setEndValue(self._blur_hover)
        self._anim_offset.setStartValue(self._sombra.offset())
        self._anim_offset.setEndValue(QPointF(0, 6))
        self._grupo.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._grupo.stop()
        self._anim_blur.setStartValue(self._sombra.blurRadius())
        self._anim_blur.setEndValue(self._blur_reposo)
        self._anim_offset.setStartValue(self._sombra.offset())
        self._anim_offset.setEndValue(QPointF(0, 2))
        self._grupo.start()
        super().leaveEvent(event)
