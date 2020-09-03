import sys
import re
import qdarkstyle
import ctypes
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtMultimedia import *
from PySide2.QtCore import *
from Project.Layouts.MainLayout import *
from Project.Layouts.PlaylistListLayout import *
from Project.Layouts.SongListLayout import *
from Project.Layouts.SongLayout import *
from Project.Player.Playlist import *
from Project.Player.MediaPlayer import *
from Project.Database.Database import PlaylistDatabase

if sys.platform == "win32":
    myappid = u"blatts1234.pyytplplayer.101"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

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
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QIcon(dir_path + "/logo.png"))

        mainLayout.addLayout(playlistListLayout, 0, 0)
        mainLayout.addLayout(songLayout, 0, 1)
        mainLayout.addLayout(songListLayout, 0, 2)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)
        self.show()

        self.selectedSongName = ""
        self.selectedPlaylistName = ""
        self.playlist = None

        self.volumeStep = 1
        self.defaultVolume = 30
        self.savedVolume = -1
        self.player = MediaPlayer(self.defaultVolume)

        songLayout.volumeLayout.setNewVolume(self.defaultVolume)
        self.player.mediaStatusChanged[QMediaPlayer.MediaStatus].connect(
            self.mediaStatusChanged)
        self.player.durationChanged.connect(self.updateDuration)
        self.player.positionChanged.connect(self.updatePosition)

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.nextSong()

    def updateDuration(self, duration):
        songLayout.songDurationLayout.setNewDuration(duration / 1000)
        songLayout.songSliderLayout.timeSlider.setMaximum(duration)

    def updatePosition(self, position):
        songLayout.songDurationLayout.setNewTime(position / 1000)
        songLayout.songSliderLayout.timeSlider.setValue(position)

    def finishPlaylistExtraction(self, playlist):
        if playlist.error:
            return

        if playlist.name == self.selectedPlaylistName:
            self.playlist = playlist
            songListLayout.setSongList(self.playlist.songs)
            self.nextSong(zeroLoop=True)

    def finishPlaylistAdding(self, playlistInfo):
        if playlistInfo["error"]:
            return

        PlaylistDatabase.addPlaylist(
            playlistInfo["title"], "https://www.youtube.com/playlist?list=" + playlistInfo["id"])
        playlistListLayout.updatePlaylists(self.playlist)

    def progressSongDownload(self, item, p):
        if p["status"] == "finished":
            item.downloadComplete()
        elif p["status"] == "downloading":
            item.downloadProgress(p["_percent_str"])

    def finishSongDownload(self, song):
        if song.error:
            self.nextSong(zeroLoop=True)
        elif song.name == self.selectedSongName:
            songLayout.songInfoLayout.setTitle(song.name)
            songLayout.playStateLayout.play()
            self.player.setMedia(song.getMediaContent())
            self.player.play()

    def selectHighlightedPlaylist(self):
        temp = playlistListLayout.selectHighlighted()
        if temp == None:
            return
        self.selectedPlaylistName = temp[1]
        playlist = Playlist(
            temp[1], temp[2], self.finishPlaylistExtraction, self.finishSongDownload)
        playlist.extractInfo()

    def selectHighlightedSong(self):
        pack = songListLayout.selectHighlighted()
        if pack == None:
            return
        songIndex, songItem = pack

        song = self.playlist.songs[songIndex]
        self.playlist.indexCurrent = songIndex
        self.selectedSongName = song.name
        songLayout.loopLayout.setNewLoop(self.playlist.loopNo())
        self.playSong(song, songItem)

    def volumeUp(self, byValue):
        self.savedVolume = -1
        songLayout.volumeLayout.setNewVolume(self.player.volumeUp(byValue))

    def volumeDown(self, byValue):
        if self.savedVolume == -1:
            songLayout.volumeLayout.setNewVolume(
                self.player.volumeDown(byValue))
        else:
            songLayout.volumeLayout.setNewVolume(
                self.player.volumeDown(byValue))

    def mute(self):
        if self.savedVolume == -1:
            self.savedVolume = self.player.volume()
            self.player.setVolume(0)
            songLayout.volumeLayout.setNewVolume(0)
        else:
            self.player.setVolume(self.savedVolume)
            songLayout.volumeLayout.setNewVolume(self.savedVolume)
            self.savedVolume = -1

    def loopUp(self):
        if self.playlist == None:
            return
        songLayout.loopLayout.setNewLoop(self.playlist.loopUp())

    def loopDown(self):
        if self.playlist == None:
            return
        songLayout.loopLayout.setNewLoop(self.playlist.loopDown())

    def loopNo(self):
        if self.playlist == None:
            return
        songLayout.loopLayout.setNewLoop(self.playlist.loopNo())

    def loopInf(self):
        if self.playlist == None:
            return
        songLayout.loopLayout.setNewLoop(self.playlist.loopInf())

    def shuffle(self):
        if self.playlist == None:
            return
        self.playlist.shuffle()
        songListLayout.setSongList(self.playlist.songs)
        self.nextSong(zeroLoop=True)

    def seek(self, byValue):
        if self.playlist == None:
            return
        self.player.setPosition(self.player.position() + byValue)

    def seekNextSong(self):
        if self.playlist == None:
            return
        self.nextSong(zeroLoop=True)

    def seekPrevSong(self):
        if self.playlist == None:
            return
        self.prevSong()

    def changePlayState(self):
        if self.player.state() == QMediaPlayer.PausedState:
            songLayout.playStateLayout.play()
            self.player.play()
        else:
            songLayout.playStateLayout.pause()
            self.player.pause()

    def addPlaylistFromClipboard(self):
        data = QApplication.clipboard().text()
        idPattern = re.compile(
            "https:\/\/www\.youtu.+list=(PL[0-9A-Za-z-_]{32})")
        if idPattern.match(data) == None:
            return

        threadpool = QThreadPool.globalInstance()
        extractor = PlaylistInfoExtarctor(data)
        extractor.signals.finished.connect(
            lambda info: self.finishPlaylistAdding(info))
        threadpool.start(extractor)

    def removeHighlightedPlaylist(self):
        playlistTemp = playlistListLayout.getHighlighted()
        if playlistTemp == None:
            return

        PlaylistDatabase.removePlaylist(playlistTemp[2])
        playlistListLayout.updatePlaylists(self.playlist)

    def keyPressEvent(self, event):
        key = event.key()
        # Playlist List
        if key == Qt.Key_Period:  # Next
            playlistListLayout.highlightNext()
        elif key == Qt.Key_Comma:  # Previous
            playlistListLayout.highlightPrevious()
        elif key == Qt.Key_Slash:  # Select
            self.selectHighlightedPlaylist()
        elif key == Qt.Key_B and (event.modifiers() & Qt.SHIFT):  # Remove Playlist
            self.removeHighlightedPlaylist()
        elif key == Qt.Key_B:  # Add Playlist
            self.addPlaylistFromClipboard()
        # Song list
        elif key == Qt.Key_Semicolon:  # Next
            songListLayout.highlightNext()
        elif key == Qt.Key_L:  # Previous
            songListLayout.highlightPrevious()
        elif key == Qt.Key_Apostrophe:  # Select
            self.selectHighlightedSong()
        elif key == Qt.Key_S and (event.modifiers() & Qt.SHIFT):  # Shuffle
            self.shuffle()
        # Volume
        elif key == Qt.Key_Plus:
            self.volumeUp(self.volumeStep)
        elif key == Qt.Key_Minus:
            self.volumeDown(self.volumeStep)
        elif key == Qt.Key_M:
            self.mute()
        # Loop
        elif key == Qt.Key_BraceRight:  # Down
            self.loopInf()
        elif key == Qt.Key_BraceLeft:  # No
            self.loopNo()
        elif key == Qt.Key_BracketRight:  # Up
            self.loopUp()
        elif key == Qt.Key_BracketLeft:  # Inf
            self.loopDown()
        # Player
        elif key == Qt.Key_Space:
            self.changePlayState()
        # Seek
        elif key == Qt.Key_D and (event.modifiers() & Qt.SHIFT):  # +1s
            self.seekNextSong()
        elif key == Qt.Key_A and (event.modifiers() & Qt.SHIFT):  # -1s
            self.seekPrevSong()
        elif key == Qt.Key_D:  # +1s
            self.seek(1000)
        elif key == Qt.Key_A:  # -1s
            self.seek(-1000)

    def nextSong(self, zeroLoop=False):
        loop, index, song = self.playlist.nextSong(zeroLoop)
        songItem = songListLayout.selectAtIndex(index)
        songLayout.loopLayout.setNewLoop(loop)
        self.selectedSongName = song.name
        self.playSong(song, songItem)

    def prevSong(self):
        index, song = self.playlist.prevSong()
        songItem = songListLayout.selectAtIndex(index)
        songLayout.loopLayout.setNewLoop("no")
        self.selectedSongName = song.name
        self.playSong(song, songItem)

    def playSong(self, song, songItem):
        if song.downloaded == False:
            song.download(songItem, self.progressSongDownload)
        else:
            songLayout.songInfoLayout.setTitle(song.name)
            songLayout.playStateLayout.play()
            self.player.setMedia(song.getMediaContent())
            self.player.play()


mainWindow = MainWindow()
app.exec_()
