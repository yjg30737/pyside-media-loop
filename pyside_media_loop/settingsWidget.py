import os

from PySide6.QtWidgets import QWidget, QLineEdit, QSpinBox, QFormLayout


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

        dirname = os.path.dirname(__file__)

        css_file_path = os.path.join(dirname, 'style/lineedit.css')
        css_file = open(css_file_path)
        css_code = css_file.read()
        css_file.close()
        self.__nameLineEdit.setStyleSheet(css_code)

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