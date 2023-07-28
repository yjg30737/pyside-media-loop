import subprocess

from PySide6.QtWidgets import QPushButton, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QApplication
from PySide6.QtCore import Qt

from pydub import AudioSegment

from pyside_media_loop.settingsWidget import SettingsWidget
from pyside_media_loop.toolWidget import ToolWidget

from pyside_media_loop.musicPlayerWidget import MusicPlayerWidget
from pyside_media_loop.findPathWidget import FindPathWidget


class MediaLoop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__play_already_flag = 0
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('Loop The Audio')
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.__findPathWidget = FindPathWidget()
        self.__findPathWidget.setLabel('File To Loop')
        self.__findPathWidget.added.connect(self.__add)

        self.__musicPlayer = MusicPlayerWidget()
        self.__musicPlayer.positionUpdated.connect(self.__positionUpdated)

        self.__toolWidget = ToolWidget()
        self.__toolWidget.croppedFrom.connect(self.__croppedFrom)
        self.__toolWidget.croppedTo.connect(self.__croppedEnd)

        self.__musicPlayer.played.connect(self.__toolWidget.setEnableToCrop)

        sliderWidget = QWidget()

        lay = QVBoxLayout()
        lay.addWidget(self.__musicPlayer)

        sliderWidget.setLayout(lay)

        self.__settingsWidget = SettingsWidget()

        self.__generateBtn = QPushButton('Generate Loop File')
        self.__generateBtn.setFixedWidth(200)

        self.__generateBtn.setEnabled(False)
        self.__generateBtn.clicked.connect(self.__generate)

        lay = QHBoxLayout()
        lay.addWidget(self.__settingsWidget)
        lay.addWidget(self.__generateBtn)
        lay.setContentsMargins(0, 0, 0, 0)
        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QHBoxLayout()
        lay.addWidget(self.__findPathWidget)
        lay.addWidget(self.__toolWidget)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(sliderWidget)
        lay.addWidget(bottomWidget)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)
        lay.setAlignment(Qt.AlignTop)

        self.setCentralWidget(mainWidget)

        self.setFixedSize(self.sizeHint())

    def __add(self, filename):
        self.__musicPlayer.setMedia(filename)
        len_of_file = self.__musicPlayer.getCurrentMediaLength()
        self.__toolWidget.setTo(len_of_file)

    def __delete(self):
        item = self.__tableWidget.currentItem()
        if item:
            self.__tableWidget.removeRow(item.row())

    def __croppedFrom(self):
        pos = self.__musicPlayer.getCurrentMediaPosition()
        self.__toolWidget.setFrom(pos)

    def __croppedEnd(self):
        pos = self.__musicPlayer.getCurrentMediaPosition()
        self.__toolWidget.setTo(pos)
        self.__generateBtn.setEnabled(True)

    def __positionUpdated(self, pos):
        self.__toolWidget.updateCropBtns(pos)

    def __generate(self):
        fromTime = self.__toolWidget.getFrom()
        toTime = self.__toolWidget.getTo()

        filename = self.__findPathWidget.getFileName()

        song = AudioSegment.from_mp3(filename)
        extract = song[fromTime:toTime]

        loopCnt = self.__settingsWidget.getLoopCount()
        filename = self.__settingsWidget.getFileName()

        # ext
        ext = 'mp3'
        filename += '.{0}'.format(ext)
        extract *= loopCnt
        extract.export(filename, format="mp3")

        path = filename.replace('/', '\\')
        subprocess.Popen(r'explorer /select,"' + path + '"')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = MediaLoop()
    ex.show()
    app.exec()