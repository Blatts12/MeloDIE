import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtMultimedia import *
from PySide2.QtCore import *
from Classes.Layout.MainLayout import *
from Classes.Layout.PlaylistListLayout import *
from Classes.Layout.SongListLayout import *
from Classes.Layout.SongLayout import *
from Classes.Player.Playlist import *


app = QApplication(sys.argv)

mainLayout = MainLayout()
playlistListLayout = PlaylistListLayout()
songLayout = SongLayout()
songListLayout = SongListLayout()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        top = 90  # 30
        left = 110  # -800
        width = 800
        height = 300
        self.setGeometry(QRect(left, top, width, height))
        self.setFixedSize(width, height)
        self.setWindowTitle("YT Playlist Player")
        self.setStyleSheet("""
            background-color: #361356;
            color: white;
        """)

        mainLayout.addLayout(playlistListLayout, 0, 0)
        mainLayout.addLayout(songLayout, 0, 1)
        mainLayout.addLayout(songListLayout, 0, 2)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.show()

        self.playlist = None
        self.selectedPlaylist = None
        self.song = None
        self.selectedSongName = None
        self.songLimit = -1
        self.songIndex = -1

        self.loop = 0

        self.player = QMediaPlayer()
        self.player.setVolume(40)
        songLayout.volumeLayout.setNewVolume(40)
        self.player.mediaStatusChanged[QMediaPlayer.MediaStatus].connect(
            self.mediaStatusChanged)
        self.player.durationChanged.connect(self.updateDuration)
        self.player.positionChanged.connect(self.updatePosition)

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            print("KONIEC")

    def updateDuration(self, duration):
        songLayout.songDurationLayout.setNewDuration(duration / 1000)
        songLayout.songSliderLayout.timeSlider.setMaximum(duration)

    def updatePosition(self, position):
        songLayout.songDurationLayout.setNewTime(position / 1000)
        songLayout.songSliderLayout.timeSlider.setValue(position)

    def loopUp(self):
        self.loop += 1
        songLayout.loopLayout.setNewLoop(self.loop)

    def loopDown(self):
        self.loop -= 1
        if self.loop <= 0:
            self.loop = 0
            songLayout.loopLayout.setNewLoop("no")
        else:
            songLayout.loopLayout.setNewLoop(self.loop)

    def loopNo(self):
        songLayout.loopLayout.setNewLoop("no")
        self.loop = 0

    def loopInf(self):
        songLayout.loopLayout.setNewLoop("inf")
        self.loop = -2

    def volumeUp(self, byValue):
        newVolume = self.player.volume() + byValue
        if newVolume > 100:
            newVolume = 100

        songLayout.volumeLayout.setNewVolume(newVolume)
        self.player.setVolume(newVolume)

    def volumeDown(self, byValue):
        newVolume = self.player.volume() - byValue
        if newVolume < 0:
            newVolume = 0

        songLayout.volumeLayout.setNewVolume(newVolume)
        self.player.setVolume(newVolume)

    def finishPlaylistExtraction(self, playlist):
        if playlist.error:
            return

        if playlist.name == self.selectedPlaylist[1]:
            self.playlist = playlist
            songListLayout.setSongList(self.playlist.songs)
            self.songLimit = len(self.playlist.songs)
            self.nextSong()

    def progressSongDownload(self, item, p):
        if p["status"] == "finished":
            item.downloadComplete()
        elif p["status"] == "downloading":
            item.downloadProgress(p["_percent_str"])

    def finishSongDownload(self, song):
        if song.error:
            self.nextSong(force=True)
            return

        if song.name == self.selectedSongName:
            self.playSong(song)

    def nextSong(self, force=False):
        if force:
            self.loopNo()

        if self.loop == 0 or self.songIndex == -1:
            newIndex = self.songIndex + 1
            self.songIndex = (newIndex, 0)[newIndex >= self.songLimit]

        if self.loop > 0:
            self.loop -= 1

        songItem = songListLayout.selectAtIndex(self.songIndex)
        self.selectedSong(songItem, self.songIndex)

    def selectedSong(self, songItem, songIndex):
        song = self.playlist.getSongFromIndex(songIndex)
        self.selectedSongName = song.name
        self.songIndex = songIndex
        self.loopNo()
        if not song.downloaded:
            song.download(songItem, self.progressSongDownload)
        else:
            self.playSong(song)

    def playSong(self, song):
        self.song = song
        url = QUrl.fromLocalFile(song.path)
        self.player.setMedia(QMediaContent(url))
        self.player.play()

    def selectHighlightedPlaylist(self):
        temp = playlistListLayout.selectHighlighted()
        if temp == None:
            return
        self.selectedPlaylist = temp
        playlist = Playlist(
            self.selectedPlaylist[1], self.selectedPlaylist[2], self.finishPlaylistExtraction, self.finishSongDownload)
        playlist.extractInfo()

    def selectHighlightedSong(self):
        pack = songListLayout.selectHighlighted()
        if pack == None:
            return
        songIndex, songItem = pack
        if songIndex == None:
            return
        self.selectedSong(songItem, songIndex)

    def keyPressEvent(self, event):
        key = event.key()
        # Playlist List
        if key == Qt.Key_Period:
            playlistListLayout.highlightNext()  # Next
        elif key == Qt.Key_Comma:
            playlistListLayout.highlightPrevious()  # Previous
        elif key == Qt.Key_Slash:  # Select
            self.selectHighlightedPlaylist()
        # Song list
        elif key == Qt.Key_Semicolon:
            songListLayout.highlightNext()  # Next
        elif key == Qt.Key_L:
            songListLayout.highlightPrevious()  # Previous
        elif key == Qt.Key_Apostrophe:
            self.selectHighlightedSong()  # Select
        # Volume
        elif key == Qt.Key_Plus:
            self.volumeUp(1)
        elif key == Qt.Key_Minus:
            self.volumeDown(1)


mainWindow = MainWindow()
app.exec_()
