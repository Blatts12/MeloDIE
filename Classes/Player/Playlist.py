import os
from pathlib import Path
from youtube_dl.utils import sanitize_filename
from PySide2.QtCore import *
from Classes.Player.SongContent import *
from ..Utils.YoutubeDL import PlaylistInfoExtarctor


class Playlist():
    def __init__(self, name, link, fpe, fsd):
        self._fpe = fpe
        self._fsd = fsd
        self.name = name
        self.link = link
        self.path = str(Path.home()) + "\\Music\\" + \
            sanitize_filename(name).strip()
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        self.songs = []
        self.error = False

    def processExtractedInfo(self, info):
        self.error = info["error"]

        if not self.error:
            for entry in info["entries"]:
                newSong = SongContent(
                    entry["id"], entry["title"], self.path, self._fsd)
                self.songs.append(newSong)

        self._fpe(self)

    def extractInfo(self):
        threadpool = QThreadPool.globalInstance()
        extractor = PlaylistInfoExtarctor(self.link)
        extractor.signals.finished.connect(
            lambda info: self.processExtractedInfo(info))
        threadpool.start(extractor)

    def getSongFromIndex(self, index):
        return self.songs[index]
