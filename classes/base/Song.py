import youtube_dl
from .Youtubedl import Ydl
from .FileManager import Filelist


class Song:
    def __init__(self, name, linkId, fileList, extension=None):
        self.name = name
        self.sanitizedName = youtube_dl.utils.sanitize_filename(name).strip()
        self.fileName = None
        self.linkId = linkId
        self.extension = extension
        self.fileList = fileList

    def setExtension(self, extension):
        self.extension = extension

    def getFilename(self):
        if self.extension == None:
            self.download()
        filename = self.sanitizedName + self.extension
        return filename

    def download(self):
        self.extension = Ydl.downloadAngGetExt(
            self.getYoutubeLink(), self.sanitizedName)
        self.fileList.append((self.sanitizedName, "." + self.extension))

    def getYoutubeLink(self):
        return "https://www.youtube.com/watch?v=" + self.linkId
