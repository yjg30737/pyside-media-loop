import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal

from fromToLblWidget import FromToLblWidget


class ToolWidget(QWidget):
    croppedFrom = Signal()
    croppedTo = Signal()

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__cropStartBtn = QPushButton()
        self.__cropStartBtn.clicked.connect(self.__croppedFrom)
        self.__cropStartBtn.setToolTip('From')

        self.__cropEndBtn = QPushButton()
        self.__cropEndBtn.clicked.connect(self.__croppedEnd)
        self.__cropEndBtn.setToolTip('To')

        dirname = os.path.dirname(__file__)

        self.__cropStartBtn.setIcon(QIcon(os.path.join(dirname, 'ico/cropStart.png')))
        self.__cropEndBtn.setIcon(QIcon(os.path.join(dirname, 'ico/cropEnd.png')))

        self.__startEndLblWidget = FromToLblWidget()

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignRight)
        lay.addWidget(self.__cropStartBtn)
        lay.addWidget(self.__cropEndBtn)
        lay.addWidget(self.__startEndLblWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)
        self.setEnableToCrop(False)

    def setEnableToCrop(self, f):
        self.__cropStartBtn.setEnabled(f)
        self.__cropEndBtn.setEnabled(f)

    def __croppedFrom(self):
        self.croppedFrom.emit()

    def __croppedEnd(self):
        self.croppedTo.emit()

    def setFrom(self, pos):
        self.__startEndLblWidget.setFrom(pos)

    def setTo(self, pos):
        self.__startEndLblWidget.setTo(pos)

    def getFrom(self):
        return self.__startEndLblWidget.getFrom()

    def getTo(self):
        return self.__startEndLblWidget.getTo()

    def updateCropBtns(self, pos):
        old_code = '''
        if pos >= self.__startEndLblWidget.getTo():
            print('current pos is bigger than to, so from shouldn\'t be checked')
            print(f'{pos} >= {self.__startEndLblWidget.getTo()}')
        elif pos <= self.__startEndLblWidget.getFrom():
            print('current pos is smaller than from, so to shouldn\'t be checked')
            print(f'{pos} <= {self.__startEndLblWidget.getFrom()}')
        print('')
        '''
