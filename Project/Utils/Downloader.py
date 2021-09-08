import yt_dlp
from PySide2.QtCore import Signal, Slot, QObject, QRunnable


class SongDownloaderSignals(QObject):
    finished = Signal(dict)
    progress = Signal(tuple)


class SongDownloader(QRunnable):
    def __init__(self, path, link, download):
        super(SongDownloader, self).__init__()
        self.signals = SongDownloaderSignals()
        self.download = download
        self.path = path
        self.link = link

    @Slot()
    def run(self):
        _ydl_opts_download = {
            "format": "bestaudio",
            "outtmpl": self.path + ".%(ext)s",
            "progress_hooks": [self.signals.progress.emit],
            "ratelimit": 512000
            # "quiet": True
        }

        with yt_dlp.YoutubeDL(_ydl_opts_download) as ydl:
            try:
                info = ydl.extract_info(
                    self.link, download=self.download, extra_info={"error": False}
                )
                self.signals.finished.emit(info)
            except Exception as e:
                self.signals.finished.emit({"error": True, "desc": e})
