import os

from PySide6.QtWidgets import QWidget, QLineEdit, QSpinBox, QFormLayout
from pyside_media_loop.resourceHelper import setStyleSheet


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__loopCntSpinBox = QSpinBox()
        self.__loopCntSpinBox.setMinimum(2)
        self.__loopCntSpinBox.setMaximum(10000)
        self.__loopCntSpinBox.setMaximumWidth(self.__loopCntSpinBox.sizeHint().width())

        self.__nameLineEdit = QLineEdit()
        self.__nameLineEdit.setMaximumWidth(self.__nameLineEdit.sizeHint().width())

        setStyleSheet([self.__nameLineEdit], ['style/lineedit.css'])

        lay = QFormLayout()
        lay.addRow('Loop Count', self.__loopCntSpinBox)
        lay.addRow('Name', self.__nameLineEdit)

        self.setLayout(lay)

    def getLineEdit(self):
        return self.__nameLineEdit
    
    def getLoopCount(self):
        return self.__loopCntSpinBox.value()

    def getFileName(self):
        return self.__nameLineEdit.text()