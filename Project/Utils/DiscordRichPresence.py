from pypresence import Presence


class DRP:
    def __init__(self):
        self.working = False
        self.playlist = "None"
        self.title = "None"
        self.time = "00:00"
        self.playState = "Paused"
        self.DRP = Presence("758697932261425222")

    def setTime(self, time):
        self.time = time
        self.setStates()

    def setTitle(self, title):
        self.title = title
        self.setStates()

    def setPlaylist(self, playlist):
        self.playlist = playlist
        self.setStates()

    def setPlayState(self, playState):
        self.playState = playState
        self.setStates()

    def start(self):
        try:
            self.DRP.connect()
            self.setStates()
            self.working = True
        except Exception as e:  # ?
            pass

    def setStates(self):
        if self.working:
            self.DRP.update(
                state=self.playState + ": " + str(self.time),
                details="[" + self.playlist + "] " + self.title,
                large_image="logo2",
            )
