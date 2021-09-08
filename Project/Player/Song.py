import glob
from youtube_dl.utils import sanitize_filename
from PySide2.QtCore import QThreadPool, QUrl
from PySide2.QtMultimedia import QMediaContent
from ..Utils.Downloader import SongDownloader


class Song:
    def __init__(self, name, ytId, playlistPath, download):
        self.name = name
        self.youtubeId = ytId
        self.audioUrl = None
        self.shouldDownload = download
        self.downloaded = False
        self.urlExtracted = False
        self.error = False

        self.path = self._getFullPath(playlistPath, sanitize_filename(name).strip())

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

    def processDownloadedSong(self, info, fsd):
        self.error = info["error"]
        if not self.error:
            if self.shouldDownload:
                self.downloaded = True
                self.path += "." + info["ext"]
            else:
                self.urlExtracted = True
                self.audioUrl = info["url"]
        fsd(self)

    def download(self, item, psd, fsd):
        threadpool = QThreadPool.globalInstance()
        downloader = SongDownloader(
            self.path, self.getYoutubeLink(), self.shouldDownload
        )
        downloader.signals.progress.connect(lambda info: psd(item, info))
        downloader.signals.finished.connect(
            lambda info: self.processDownloadedSong(info, fsd)
        )
        threadpool.start(downloader)

    def getMediaContent(self):
        if self.shouldDownload or self.downloaded:
            return QMediaContent(QUrl.fromLocalFile(self.path))
        else:
            return QMediaContent(QUrl(self.audioUrl))
