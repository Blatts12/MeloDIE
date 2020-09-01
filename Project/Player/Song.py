import glob
from youtube_dl.utils import sanitize_filename
from PySide2.QtCore import *
from PySide2.QtMultimedia import *
from ..Utils.Downloader import *


class Song:
    def __init__(self, name, ytId, playlistPath, fsd):
        self._finishSongDownload = fsd

        self.name = name
        self.youtubeId = ytId

        self.downloaded = False
        self.error = False

        self.path = self._getFullPath(
            playlistPath, sanitize_filename(name).strip())

    def _getFullPath(self, playlistPath, sanitizedName):
        path = playlistPath + "\\" + sanitizedName
        files = glob.glob(path.replace("[", "[[]") + ".*")
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

        self._finishSongDownload(self)

    def download(self, item, psd):
        threadpool = QThreadPool.globalInstance()
        downloader = SongDownloader(self.path, self.getYoutubeLink())
        downloader.signals.progress.connect(lambda info: psd(item, info))
        downloader.signals.finished.connect(
            lambda info: self.processDownloadedSong(info))
        threadpool.start(downloader)

    def getMediaContent(self):
        return QMediaContent(QUrl.fromLocalFile(self.path))
