from PySide2.QtCore import *
from youtube_dl.utils import sanitize_filename
from ..Utils.FileChecker import FlieChecker
from ..Utils.YoutubeDL import SongDownloader


class SongContent:
    def __init__(self, ytId, name, playlistPath, fsd):
        self._fileChecker = FlieChecker()
        self._fsd = fsd
        self.youtubeId = ytId
        self.name = name
        self.downloaded = False
        self.error = False
        self.path = self._getFullPath(
            playlistPath, sanitize_filename(name).strip())

    def _getFullPath(self, playlistPath, sanitizedName):
        path = playlistPath + "\\" + sanitizedName
        files = self._fileChecker.getFile(path)
        if files == []:
            return path
        else:
            self.downloaded = True
            return files[0]

    def getYoutubeLink(self):
        return "https://www.youtube.com/watch?v=" + self.youtubeId

    def processDownloadedSong(self, info):
        self.error = info["error"]
        if not self.error:
            self.downloaded = True
            self.path += "." + info["ext"]

        self._fsd(self)

    def download(self, item, psd):
        threadpool = QThreadPool.globalInstance()
        downloader = SongDownloader(self.path, self.getYoutubeLink())
        downloader.signals.progress.connect(lambda info: psd(item, info))
        downloader.signals.finished.connect(
            lambda info: self.processDownloadedSong(info))
        threadpool.start(downloader)
