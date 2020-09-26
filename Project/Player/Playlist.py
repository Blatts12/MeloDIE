import random
import os
from pathlib import Path
from youtube_dl.utils import sanitize_filename
from ..Utils.Extractor import PlaylistInfoExtarctor
from PySide2.QtCore import *
from .Song import Song


class Playlist:
    def __init__(self, name, link, download):
        self.name = name
        self.link = link
        self.download = download
        self.path = self._setPath()

        self.songs = []
        self.loop = 0
        self.indexCurrent = -1
        self.indexLimit = -1

        self.error = False

    def _setPath(self):
        path = "C:/_Muzyka/" + sanitize_filename(self.name).strip()
        # path = str(Path.home()) + "/Music/" + sanitize_filename(self.name).strip()

        if not os.path.isdir(path):
            os.mkdir(path)

        return path

    def songAtIndex(self, index):
        self.indexCurrent = index
        self.loop = 0
        return self.songs[index]

    def nextSong(self, zeroLoop):
        if zeroLoop == True:
            self.loop = 0

        if self.loop == 0 or self.indexCurrent == -1:
            newIndex = self.indexCurrent + 1
            self.indexCurrent = (newIndex, 0)[newIndex >= self.indexLimit]
        elif self.loop > 0:
            self.loop -= 1

        return (self.loopString(), self.indexCurrent, self.songs[self.indexCurrent])

    def prevSong(self):
        newIndex = self.indexCurrent - 1
        self.indexCurrent = (newIndex, self.indexLimit - 1)[newIndex < 0]
        self.loop = 0
        return (self.indexCurrent, self.songs[self.indexCurrent])

    def shuffle(self):
        random.shuffle(self.songs)
        self.indexCurrent = -1
        return self.songs

    def loopDown(self):
        self.loop = (self.loop - 1, 0)[self.loop <= 0]
        if self.loop == 0:
            return "no"
        return str(self.loop)

    def loopUp(self):
        if self.loop == -1:
            return "inf"
        self.loop += 1
        return str(self.loop)

    def loopNo(self):
        self.loop = 0
        return "no"

    def loopInf(self):
        self.loop = -1
        return "inf"

    def loopString(self):
        if self.loop == 0:
            return "no"
        elif self.loop == -1:
            return "inf"
        else:
            return str(self.loop)

    def processExtractedInfo(self, info, fpe):
        self.error = info["error"]

        if not self.error:
            for entry in info["entries"]:
                newSong = Song(entry["title"], entry["id"], self.path, self.download)
                self.songs.append(newSong)

            self.indexLimit = len(self.songs)

        fpe(self)

    def extractInfo(self, fpe):
        threadpool = QThreadPool.globalInstance()
        extractor = PlaylistInfoExtarctor(self.link)
        extractor.signals.finished.connect(
            lambda info: self.processExtractedInfo(info, fpe)
        )
        threadpool.start(extractor)
