import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QLabel, QApplication

from pyside_media_loop.findPathLineEdit import FindPathLineEdit


class FindPathWidget(QWidget):
    findClicked = Signal()
    added = Signal(str)

    def __init__(self, default_filename: str = ''):
        super().__init__()
        self.__initVal()
        self.__initUi(default_filename)

    def __initVal(self):
        self.__ext_of_files = ''
        self.__directory = False

    def __initUi(self, default_filename: str = ''):
        self.__pathLineEdit = FindPathLineEdit()
        if default_filename:
            self.__pathLineEdit.setText(default_filename)

        self.__pathFindBtn = QPushButton('Find...')

        dirname = os.path.dirname(__file__)

        css_file_path = os.path.join(dirname, 'style/lineedit.css')
        css_file = open(css_file_path)
        css_code = css_file.read()
        css_file.close()

        self.__pathLineEdit.setStyleSheet(css_code)

        css_file_path = os.path.join(dirname, 'style/button.css')
        css_file = open(css_file_path)
        css_code = css_file.read()
        css_file.close()

        self.__pathFindBtn.setStyleSheet(css_code)

        self.__pathFindBtn.clicked.connect(self.__find)

        self.__pathLineEdit.setMaximumHeight(self.__pathFindBtn.sizeHint().height())

        lay = QHBoxLayout()
        lay.addWidget(self.__pathLineEdit)
        lay.addWidget(self.__pathFindBtn)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def setLabel(self, text):
        self.layout().insertWidget(0, QLabel(text))

    def setExtOfFiles(self, ext_of_files):
        self.__ext_of_files = ext_of_files

    def getLineEdit(self):
        return self.__pathLineEdit

    def getButton(self):
        return self.__pathFindBtn

    def getFileName(self):
        return self.__pathLineEdit.text()

    def setCustomFind(self, f: bool):
        if f:
            self.__pathFindBtn.clicked.disconnect(self.__find)
            self.__pathFindBtn.clicked.connect(self.__customFind)

    def __customFind(self):
        self.findClicked.emit()

    def __find(self):
        if self.isForDirectory():
            dirname = QFileDialog.getExistingDirectory(None, 'Open Directory', '', QFileDialog.ShowDirsOnly)
            if dirname:
                self.__pathLineEdit.setText(dirname)
                self.added.emit(dirname)
        else:
            str_exp_files_to_open = self.__ext_of_files if self.__ext_of_files else 'All Files (*.*)'
            filename = QFileDialog.getOpenFileName(self, 'Find', '', str_exp_files_to_open)
            if filename[0]:
                filename = filename[0]
                self.__pathLineEdit.setText(filename)
                self.added.emit(filename)

    def setAsDirectory(self, f: bool):
        self.__directory = f

    def isForDirectory(self) -> bool:
        return self.__directory


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = FindPathWidget()
    ex.show()
    sys.exit(app.exec_())

