from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt


class FromToLblWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__cur_len = 0
        self.__from_pos = 0
        self.__to_pos = 0
        self.__initUi()

    def __initUi(self):
        self.__fromLbl = QLabel('00:00:00')
        self.__toLbl = QLabel('00:00:00')

        self.__fromLbl.setAlignment(Qt.AlignCenter)
        self.__toLbl.setAlignment(Qt.AlignCenter)

        self.__fromLbl.setStyleSheet('QLabel {'
                                'border: 1px solid #DDD; '
                               'border-top-left-radius: 10px;'
                               'border-bottom-left-radius: 10px;'
                               'padding: 5px;}')

        self.__toLbl.setStyleSheet('QLabel {'
                                'border: 1px solid #DDD; '
                               'border-top-right-radius: 10px;'
                               'border-bottom-right-radius: 10px;'
                               'padding: 5px;}')

        lay = QHBoxLayout()
        lay.addWidget(self.__fromLbl)
        lay.addWidget(self.__toLbl)
        lay.setSpacing(0)

        lblWidget = QWidget()
        lblWidget.setLayout(lay)

        lay = lblWidget.layout()
        lay.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lay)

    def __formatTime(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = round(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24

        # todo "%02d:%02d:%02d:%02d" % (hours, minutes, seconds, millisecond)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def setFrom(self, pos):
        if self.__isTo():
            if pos >= self.__to_pos:
                # todo set end_pos to very end of music
                pass
        else:
            # todo set end_pos to very end of music as well
            pass

        self.__from_pos = pos
        self.__fromLbl.setText(self.__formatTime(pos))

    def setTo(self, pos):
        if self.__isFrom():
            if self.__from_pos >= pos:
                # todo set start_pos to very start of music
                pass
        else:
            # todo set start_pos to very start of music as well
            pass
        self.__to_pos = pos
        self.__toLbl.setText(self.__formatTime(pos))

    def getFrom(self):
        return self.__from_pos

    def getTo(self):
        return self.__to_pos

    def __isFrom(self):
        return self.__from_pos

    def __isTo(self):
        return self.__to_pos