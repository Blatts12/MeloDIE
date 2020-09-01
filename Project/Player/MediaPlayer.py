from PySide2.QtMultimedia import *


class MediaPlayer(QMediaPlayer):
    def __init__(self, defaultVolume, *args, **kwargs):
        super(MediaPlayer, self).__init__(*args, **kwargs)
        self.setVolume(defaultVolume)

    def volumeUp(self, byValue):
        newVolume = self.volume() + byValue
        if newVolume > 100:
            newVolume = 100

        self.setVolume(newVolume)
        return newVolume

    def volumeDown(self, byValue):
        newVolume = self.volume() - byValue
        if newVolume < 0:
            newVolume = 0

        self.setVolume(newVolume)
        return newVolume
