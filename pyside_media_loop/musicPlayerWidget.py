import os

from PySide6.QtGui import QIcon
from mutagen import mp3

from PySide6.QtCore import QUrl, Signal
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton

from mediaSlider import MediaSlider
from PySide6.QtCore import Qt


class MusicPlayerWidget(QWidget):
    played = Signal(bool)
    positionUpdated = Signal(int)
    durationUpdated = Signal(int)

    def __init__(self, slider=None):
        super().__init__()
        self.__initUi(slider)

    def __initUi(self, slider=None):
        self.__audio_output = QAudioOutput()
        self.__mediaPlayer = QMediaPlayer()
        self.__mediaPlayer.setAudioOutput(self.__audio_output)

        self.__timerLbl = QLabel()
        self.__curLenLbl = QLabel()

        self.__slider = slider if slider else MediaSlider()
        self.__slider.pressed.connect(self.__handlePressed)
        self.__slider.dragged.connect(self.__handleDragged)
        self.__slider.released.connect(self.__handleReleased)

        self.__zeroTimeStr = '00:00:00'
        self.__currentMediaDuration = 0

        self.__timerLbl.setText(self.__zeroTimeStr)
        self.__curLenLbl.setText(self.__zeroTimeStr)

        lay = QHBoxLayout()
        lay.addWidget(self.__timerLbl)
        lay.addWidget(self.__slider)
        lay.addWidget(self.__curLenLbl)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        dirname = os.path.dirname(__file__)

        self.__playBtn = QPushButton()
        self.__playBtn.setIcon(QIcon(os.path.join(dirname, 'ico/play.png')))
        self.__playBtn.setObjectName('play')
        self.__playBtn.setEnabled(False)

        self.__stopBtn = QPushButton()
        self.__stopBtn.setIcon(QIcon(os.path.join(dirname, 'ico/stop.png')))
        self.__stopBtn.setEnabled(False)

        btns = [self.__playBtn, self.__stopBtn]

        self.__playBtn.clicked.connect(self.__togglePlayback)
        self.__stopBtn.clicked.connect(self.stop)

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignCenter)
        for btn in btns:
            lay.addWidget(btn)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(bottomWidget)
        lay.setContentsMargins(2, 2, 2, 2)

        self.setLayout(lay)

        self.__mediaPlayer.positionChanged.connect(self.__updatePosition)
        self.__mediaPlayer.durationChanged.connect(self.__updateDuration)

    def __getMediaLengthHumanFriendly(self, filename):
        audio = mp3.MP3(filename)
        media_length = audio.info.length
        self.__currentMediaDuration = media_length

        # convert second into hh:mm:ss
        h = int(media_length / 3600)
        media_length -= (h * 3600)
        m = int(media_length / 60)
        media_length -= (m * 60)
        s = media_length
        song_length = '{:0>2d}:{:0>2d}:{:0>2d}'.format(int(h), int(m), int(s))

        return song_length

    def __handlePressed(self, pos):
        self.__mediaPlayer.pause()
        self.__setPosition(pos)

    def __handleDragged(self, pos):
        self.__timerLbl.setText(self.__formatTime(pos))

    def __handleReleased(self, pos):
        self.__setPosition(pos)
        if self.__playBtn.objectName() == 'play':
            pass
        else:
            self.__mediaPlayer.play()

    def __setPosition(self, pos):
        self.__mediaPlayer.setPosition(pos)

    # convert millisecond into hh:mm:ss
    def __formatTime(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24

        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def __updatePosition(self, pos):
        self.__slider.setValue(pos)
        if pos == self.__slider.maximum():
            self.stop()
        self.__timerLbl.setText(self.__formatTime(pos))
        self.positionUpdated.emit(pos)

    def __updateDuration(self, duration):
        self.__slider.setRange(0, duration)
        self.__slider.setEnabled(duration > 0)
        self.__slider.setPageStep(duration / 1000)
        self.durationUpdated.emit(duration)

    def setMedia(self, filename):
        mediaContent = QUrl.fromLocalFile(filename)  # it also can be used as playlist
        self.__mediaPlayer.setSource(mediaContent)
        self.__playBtn.setEnabled(True)
        self.__curLenLbl.setText(self.__getMediaLengthHumanFriendly(filename))

    def getCurrentMediaPosition(self):
        return self.__mediaPlayer.position()

    def getCurrentMediaLength(self):
        return self.__mediaPlayer.duration()

    def play(self):
        dirname = os.path.dirname(__file__)

        self.__playBtn.setIcon(QIcon(os.path.join(dirname, 'ico/pause.png')))
        self.__playBtn.setObjectName('pause')
        self.__mediaPlayer.play()
        self.played.emit(True)
        self.__stopBtn.setEnabled(True)

    def pause(self):
        dirname = os.path.dirname(__file__)

        self.__playBtn.setIcon(QIcon(os.path.join(dirname, 'ico/play.png')))
        self.__playBtn.setObjectName('play')
        self.__mediaPlayer.pause()

    def __togglePlayback(self):
        if self.__mediaPlayer.mediaStatus() == QMediaPlayer.NoMedia:
            pass  # or openFile()
        elif self.__mediaPlayer.playbackState() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def stop(self):
        dirname = os.path.dirname(__file__)

        self.__playBtn.setIcon(QIcon(os.path.join(dirname, 'ico/play.png')))
        self.__playBtn.setObjectName('play')
        self.__mediaPlayer.stop()
        self.__stopBtn.setEnabled(False)
        self.played.emit(False)