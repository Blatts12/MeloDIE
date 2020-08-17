import youtube_dl
import random
import os
from .Youtubedl import Ydl
from .Song import Song
from .FileManager import Fm, Filelist
from .. import config


class Playlist:
    @staticmethod
    def getPlaylistTitleFromLink(link):
        infoDict = Ydl.getInfoPlaylist(link)
        return infoDict["title"]

    def __init__(self, name, link, prepareInfo=False):
        self.name = name
        self.sanitizedName = youtube_dl.utils.sanitize_filename(name).strip()
        self.link = link
        self.uploader = None

        self.path = config.paths["music"] + "\\" + self.sanitizedName
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

        self.songs = []
        self.fileList = Filelist(Fm.getFileExtList(self.path))
        self.indexPlaying = -1
        self.indexLimit = 0
        self.loopSong = 0  # -1 = inf
        if prepareInfo == False:
            return
        self.prepareInfo()

    def prepareInfo(self):
        infoDict = Ydl.getInfoPlaylist(self.link)
        self.uploader = infoDict["uploader"]
        self.getSongListFromInfoDict(infoDict["entries"])
        Ydl.changePlaylist(self.path)

    def getSongListFromInfoDict(self, entries):
        for song in entries:
            newSong = Song(song["title"], song["id"], self.fileList)
            ext = Fm.fileAndExtFromSong(
                newSong.sanitizedName, self.fileList.getFileList())
            ext = None if ext == [] else ext[0]
            newSong.setExtension(ext)
            self.songs.append(newSong)

        self.indexLimit = len(self.songs)

    def setLoop(self, loop):
        ''' -1 = inf '''
        if loop == -2:
            self.loopSong = -1
            return -1
        elif loop == 0:
            self.loopSong = loop
            return 0
        else:
            self.loopSong += loop
            if self.loopSong < 0:
                self.loopSong = 0

            return self.loopSong

    def shuffle(self):
        random.shuffle(self.songs)
        self.indexPlaying = -1
        self.loopSong = 0

    def _getReturnDict(self, index, loop, filename, title):
        return dict(
            index=index,
            loop=loop,
            filename=filename,
            title=title,
            path=self.path,
        )

    def playNextSong(self):
        if self.loopSong == 0 or self.indexPlaying == -1:
            newIndex = self.indexPlaying + 1
            self.indexPlaying = (newIndex, 0)[newIndex >= self.indexLimit]

        if self.loopSong == -1:  # inf loop
            return self._getReturnDict(self.indexPlaying, self.loopSong, self.songs[self.indexPlaying].getFilename(), self.songs[self.indexPlaying].name)
        elif self.loopSong > 0:  # loop
            self.loopSong -= 1
            return self._getReturnDict(self.indexPlaying, self.loopSong, self.songs[self.indexPlaying].getFilename(), self.songs[self.indexPlaying].name)
        else:  # no loop
            return self._getReturnDict(self.indexPlaying, self.loopSong, self.songs[self.indexPlaying].getFilename(), self.songs[self.indexPlaying].name)

    def playPreviousSongSimple(self):
        newIndex = self.indexPlaying - 1
        self.indexPlaying = (newIndex, self.indexLimit - 1)[newIndex < 0]
        return self._getReturnDict(self.indexPlaying, self.loopSong, self.songs[self.indexPlaying].getFilename(), self.songs[self.indexPlaying].name)

    def playNextSongSimple(self):
        newIndex = self.indexPlaying + 1
        self.indexPlaying = (newIndex, 0)[newIndex >= self.indexLimit]
        return self._getReturnDict(self.indexPlaying, self.loopSong, self.songs[self.indexPlaying].getFilename(), self.songs[self.indexPlaying].name)

    def playSongAtIndex(self, index):
        self.loopSong = 0
        self.indexPlaying = index
        return self._getReturnDict(self.indexPlaying, self.loopSong, self.songs[self.indexPlaying].getFilename(), self.songs[self.indexPlaying].name)
