from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from youtube_dl.downloader.common import FileDownloader


class MyLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(MyLabel, self).__init__(*args, **kwargs)
        font = QFont()
        font.setPixelSize(17)
        self.setFont(font)
        self.setStyleSheet("""
            QLabel {
                border: 1px solid #32414B;
                border-radius: 4px;
            }
            QLabel:hover {
                border: 1px solid #148CD2;
            }
        """)


class TimeSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super(TimeSlider, self).__init__(*args, **kwargs)
        self.setFixedWidth(360)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            return
        super(TimeSlider, self).keyPressEvent(event)


class SongInfoLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SongInfoLayout, self).__init__(*args, **kwargs)
        self._titleLabel = MyLabel("None")
        self._titleLabel.setWordWrap(True)
        self.addWidget(self._titleLabel)

    def setTitle(self, title):
        self._titleLabel.setText(title)


class SongSliderLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SongSliderLayout, self).__init__(*args, **kwargs)
        self.timeSlider = TimeSlider(Qt.Horizontal)

        self.addWidget(self.timeSlider)
        self.setAlignment(self.timeSlider, Qt.AlignCenter)


class SongDurationLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SongDurationLayout, self).__init__(*args, **kwargs)
        self._timeText = "00:00:00"
        self._durationText = "00:00:00"
        self._timeLabel = MyLabel(self._timeText + " / " + self._durationText)
        self._timeLabel.setAlignment(Qt.AlignCenter)
        self._timeLabel.setFixedWidth(190)
        self.addWidget(self._timeLabel)
        self.setAlignment(self._timeLabel, Qt.AlignCenter)

    def setNewDuration(self, dur):
        self._durationText = FileDownloader.format_seconds(dur)
        self._timeLabel.setText(self._timeText + " / " + self._durationText)

    def setNewTime(self, time):
        self._timeText = FileDownloader.format_seconds(time)
        self._timeLabel.setText(self._timeText + " / " + self._durationText)


class VolumeLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(VolumeLayout, self).__init__(*args, **kwargs)
        self._volumeLabel = MyLabel("Volume: X%")
        self._volumeLabel.setFixedWidth(190)
        self._volumeLabel.setAlignment(Qt.AlignCenter)
        self.addWidget(self._volumeLabel)
        self.setAlignment(self._volumeLabel, Qt.AlignCenter)

    def setNewVolume(self, volume):
        self._volumeLabel.setText("Volume: " + str(volume) + "%")


class LoopLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(LoopLayout, self).__init__(*args, **kwargs)
        self._loopLabel = MyLabel("Loop: no")
        self._loopLabel.setFixedWidth(190)
        self._loopLabel.setAlignment(Qt.AlignCenter)
        self.addWidget(self._loopLabel)
        self.setAlignment(self._loopLabel, Qt.AlignCenter)

    def setNewLoop(self, loop):
        self._loopLabel.setText("Loop: " + loop)


class PlayStateLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(PlayStateLayout, self).__init__(*args, **kwargs)
        self._stateLabel = MyLabel("Paused")
        self._stateLabel.setFixedWidth(190)
        self._stateLabel.setAlignment(Qt.AlignCenter)
        self.addWidget(self._stateLabel)
        self.setAlignment(self._stateLabel, Qt.AlignCenter)

    def pause(self):
        self._stateLabel.setText("Paused")

    def play(self):
        self._stateLabel.setText("Playing")


class SongLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(SongLayout, self).__init__(*args, **kwargs)

        self.setRowStretch(0, 125)
        self.setRowStretch(1, 50)
        self.setRowStretch(2, 75)
        self.setRowStretch(2, 50)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setSpacing(0)

        self.songInfoLayout = SongInfoLayout()
        self.playStateLayout = PlayStateLayout()
        self.loopLayout = LoopLayout()
        self.songSliderLayout = SongSliderLayout()
        self.songDurationLayout = SongDurationLayout()
        self.volumeLayout = VolumeLayout()

        self.addLayout(self.songInfoLayout, 0, 0, 1, 2)
        self.addLayout(self.playStateLayout, 1, 0, 1, 1)
        self.addLayout(self.loopLayout, 1, 1, 1, 1)
        self.addLayout(self.songSliderLayout, 2, 0, 1, 2)
        self.addLayout(self.songDurationLayout, 3, 0, 1, 1)
        self.addLayout(self.volumeLayout, 3, 1, 1, 1)
