import yt_dlp
from PySide2.QtCore import Signal, Slot, QObject, QRunnable


class PlaylistInfoExtarctorSignals(QObject):
    finished = Signal(dict)


class PlaylistInfoExtarctor(QRunnable):
    def __init__(self, link):
        super(PlaylistInfoExtarctor, self).__init__()
        self.signals = PlaylistInfoExtarctorSignals()
        self._ydl_opts_info = {
            "format": "bestaudio/best",
            "extract_flat": True,
            "dump_single_json": True,
        }
        self.link = link

    @Slot()
    def run(self):
        with yt_dlp.YoutubeDL(self._ydl_opts_info) as ydl:
            try:
                info = ydl.extract_info(self.link, download=False)
                info["error"] = False
                self.signals.finished.emit(info)
            except Exception as e:
                self.signals.finished.emit({"error": True, "desc": e})


class SongAudioLinkExtractorSignals(QObject):
    finished = Signal(dict)


class SongAudioLinkExtractor(QRunnable):
    def __init__(self, link):
        super(SongAudioLinkExtractor, self).__init__()
        self.signals = SongAudioLinkExtractorSignals()
        self._ydl_opts_info = {
            "format": "bestaudio/best",
            "forceurl": True,
            "dump_single_json": True,
        }
        self.link = link

    @Slot()
    def run(self):
        with yt_dlp.YoutubeDL(self._ydl_opts_info) as ydl:
            try:
                info = ydl.extract_info(self.link, download=False)
                info["error"] = False
                self.signals.finished.emit(info)
            except Exception as e:
                self.signals.finished.emit({"error": True, "desc": e})
