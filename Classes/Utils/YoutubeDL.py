import youtube_dl
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class SongDownloaderSignals(QObject):
    finished = Signal(dict)
    progress = Signal(tuple)


class SongDownloader(QRunnable):
    def __init__(self, path, link):
        super(SongDownloader, self).__init__()
        self.signals = SongDownloaderSignals()
        self.path = path
        self.link = link

    @Slot()
    def run(self):
        _ydl_opts_download = {
            "format": "bestaudio",
            "outtmpl": self.path + ".%(ext)s",
            "progress_hooks": [self.signals.progress.emit],
            # "quiet": True
        }

        with youtube_dl.YoutubeDL(_ydl_opts_download) as ydl:
            try:
                info = ydl.extract_info(
                    self.link, download=True, extra_info={"error": False})
                self.signals.finished.emit(info)
            except Exception as e:
                self.signals.finished.emit({"error": True, "desc": e})


class PlaylistInfoExtarctorSignals(QObject):
    finished = Signal(dict)


class PlaylistInfoExtarctor(QRunnable):
    def __init__(self, link):
        super(PlaylistInfoExtarctor, self).__init__()
        self.signals = PlaylistInfoExtarctorSignals()
        self._ydl_opts_info = {
            "format": "bestaudio/best",
            "extract_flat": True,
            "dump_single_json": True
        }
        self.link = link

    @Slot()
    def run(self):
        with youtube_dl.YoutubeDL(self._ydl_opts_info) as ydl:
            try:
                info = ydl.extract_info(self.link, download=False)
                info["error"] = False
                self.signals.finished.emit(info)
            except Exception as e:
                self.signals.finished.emit({"error": True, "desc": e})
