import mpv
from .. import config


def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))


class Player:
    def __init__(self):
        self.Instance = mpv.MPV(video=False, ytdl=False, log_handler=my_log)
        self.volume = config.player["volume_start"]
        self.volumeStep = config.player["volume_step"]
        self.volumeMax = config.player["volume_max"]

        self.Instance._set_property("volume", float(self.volume))
        self.Instance.pause = False

    def volumeUp(self):
        if self.volume == self.volumeMax:
            return self.volume

        newVolume = self.volume + self.volumeStep
        newVolume = (newVolume, self.volumeMax)[newVolume > self.volumeMax]

        self.volume = newVolume
        self.Instance._set_property("volume", float(self.volume))
        return self.volume

    def volumeDown(self):
        if self.volume == 0:
            return self.volume

        newVolume = self.volume - self.volumeStep
        newVolume = (newVolume, 0)[newVolume < 0]

        self.volume = newVolume
        self.Instance._set_property("volume", float(self.volume))
        return self.volume


Player = Player()
