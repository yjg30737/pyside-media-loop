import os

from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt, Signal

from pyside_media_loop.resourceHelper import setStyleSheet


class MediaSlider(QSlider):
    pressed = Signal(int)
    dragged = Signal(int)
    released = Signal(int)

    def __init__(self):
        super().__init__()
        self.__pressed = False
        self.__initUi()

    def __initUi(self):
        self.setOrientation(Qt.Horizontal)

        setStyleSheet([self], ['style/slider.css'])

        self.setRange(0, 10000)

        self.setMouseTracking(True)

    def __setPositionAndGetValue(self, e):
        x = e.pos().x()

        mid = self.width() / 2

        if x > mid:
            x += min(4, (x - mid) / (mid / 4))
        elif mid > x > 0:
            x -= min(4, mid / x)

        value = self.minimum() + (self.maximum() - self.minimum()) * x / self.width()
        if value < 0:
            value = 0
        elif value >= self.maximum():
            value = self.maximum()
        self.setValue(value)
        return value

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__pressed = True
            e.accept()
            value = self.__setPositionAndGetValue(e)
            self.pressed.emit(value)

    def mouseMoveEvent(self, e):
        if self.__pressed:
            e.accept()
            value = self.__setPositionAndGetValue(e)
            self.dragged.emit(value)
        return super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__pressed = False
            e.accept()
            value = self.__setPositionAndGetValue(e)
            self.released.emit(value)
        return super().mouseReleaseEvent(e)