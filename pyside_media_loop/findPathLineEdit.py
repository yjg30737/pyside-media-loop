import subprocess

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QMenu


class FindPathLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.setMouseTracking(True)
        self.setReadOnly(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__prepareMenu)

    def mouseMoveEvent(self, e):
        self.__showToolTip()
        return super().mouseMoveEvent(e)

    def __showToolTip(self):
        text = self.text()
        text_width = self.fontMetrics().boundingRect(text).width()

        if text_width > self.width():
            self.setToolTip(text)
        else:
            self.setToolTip('')

    def __prepareMenu(self, pos):
        menu = QMenu(self)
        openDirAction = QAction('Open Path')
        openDirAction.setEnabled(self.text().strip() != '')
        openDirAction.triggered.connect(self.__openPath)
        menu.addAction(openDirAction)
        menu.exec(self.mapToGlobal(pos))

    def __openPath(self):
        filename = self.text()
        path = filename.replace('/', '\\')
        subprocess.Popen(r'explorer /select,"' + path + '"')