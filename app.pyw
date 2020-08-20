import sys
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PySide2.QtGui import QIcon
from PySide2.QtCore import QRect, QMargins, Qt
from classes.layout.MainLayout import MainLayout
from classes.layout.PlaylistListLayout import PlaylistListLayout
from classes.layout.SongLayout import SongLayout
from classes.layout.SongListLayout import SongListLayout
from classes.base.Playlist import Playlist
from classes.base.Player import Player
from classes.base.Youtubedl import Ydl
from classes import config

app = QApplication(sys.argv)


mainLayout = MainLayout()
playlistListLayout = PlaylistListLayout()
songLayout = SongLayout()
songListLayout = SongListLayout()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.playlist = None
        self.stopNumber = 2
        self.stopChange = False
        self.stopStopChange = True
        self.setWindowTitle(config.window["title"])
        self.setWindowIcon(QIcon("logo.png"))
        top = 90  # 30
        left = 110  # -800
        width = 800
        height = 300
        self.setGeometry(QRect(left, top, width, height))
        self.setFixedSize(width, height)
        self.setStyleSheet("""
            background-color: #{bg};
            color: white;
        """.format(
            bg=config.colors["background"]
        ))

        mainLayout.addLayout(playlistListLayout, 0, 0)
        mainLayout.addLayout(songLayout, 0, 1)
        mainLayout.addLayout(songListLayout, 0, 2)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def keyPressEvent(self, event):
        key = event.key()
        # Playlist List
        if key == Qt.Key_Period:
            playlistListLayout.highlightNext()  # Next
        elif key == Qt.Key_Comma:
            playlistListLayout.highlightPrevious()  # Previous
        elif key == Qt.Key_Slash:
            self.selectHighlightedPlaylist()  # Select
        # Song list
        elif key == Qt.Key_Semicolon:
            songListLayout.highlightNext()  # Next
        elif key == Qt.Key_L:
            songListLayout.highlightPrevious()  # Previous
        elif key == Qt.Key_Apostrophe:
            self.selectHighlightedSong()  # Select
        # Player
        elif key == Qt.Key_Space:  # Pause
            self.pause()
        elif key == Qt.Key_S:  # Shuffle
            self.shuffle()
        # Loop
        elif key == Qt.Key_BraceRight:  # -1
            self.changeLoop(-2)
        elif key == Qt.Key_BraceLeft:  # no
            self.changeLoop(0)
        elif key == Qt.Key_BracketRight:  # +1
            self.changeLoop(1)
        elif key == Qt.Key_BracketLeft:  # inf
            self.changeLoop(-1)
        # Volume
        elif key == Qt.Key_Plus:  # UP
            self.volume(True)
        elif key == Qt.Key_Minus:  # DOWN
            self.volume(False)
        # Song
        elif key == Qt.Key_D and (event.modifiers() & Qt.SHIFT):
            self.forceNextSong()
        elif key == Qt.Key_A and (event.modifiers() & Qt.SHIFT):
            self.forcePreviousSong()
        # Seek
        elif key == Qt.Key_D:  # +1
            self.seek(1)
        elif key == Qt.Key_A:  # -1
            self.seek(-1)

    def selectHighlightedPlaylist(self):
        playlist = playlistListLayout.selectHighlighted()
        if playlist == None:
            return
        self.playlist = Playlist(
            playlist[1], playlist[2], prepareInfo=True)
        songListLayout.setSongList(self.playlist.songs)
        self.stopNumber -= 1
        Player.Instance.pause = False
        self.setLoopText(0)
        songLayout.playStateLayout.play()
        self.nextSong()

    def selectHighlightedSong(self):
        index = songListLayout.selectHighlighted()
        if index == None:
            return
        self.stopNumber -= 1
        songDict = self.playlist.playSongAtIndex(index)
        path = songDict["path"] + "\\" + songDict["filename"]
        Player.Instance.pause = False
        self.setLoopText(0)
        songLayout.songInfoLayout.setNewTitle(songDict["title"])
        songLayout.playStateLayout.play()
        Player.Instance.play(path)

    def pause(self):
        Player.Instance.pause = not Player.Instance.pause
        if Player.Instance.pause == True:
            songLayout.playStateLayout.pause()
        else:
            songLayout.playStateLayout.play()

    def volume(self, index):
        if index == True:
            songLayout.volumeLayout.setNewVolume(Player.volumeUp())
        else:
            songLayout.volumeLayout.setNewVolume(Player.volumeDown())

    def seek(self, value):
        if Player.Instance._get_property("seekable") == None:
            return
        Player.Instance.seek(value)

    def shuffle(self):
        if self.playlist == None:
            return
        self.playlist.shuffle()
        songListLayout.setSongList(self.playlist.songs)
        self.stopNumber -= 1
        self.setLoopText(0)
        self.nextSong()

    def changeLoop(self, loopChange):
        if self.playlist == None:
            return
        loop = self.playlist.setLoop(loopChange)
        self.setLoopText(loop)

    def setLoopText(self, loop):
        if loop == 0:
            songLayout.loopLayout.setNewLoop("no")
        elif loop == -1:
            songLayout.loopLayout.setNewLoop("inf")
        else:
            songLayout.loopLayout.setNewLoop(str(loop))

    def nextSong(self):
        songDict = mainWindow.playlist.playNextSongSimple()
        self._setSong(songDict)

    def previousSong(self):
        songDict = mainWindow.playlist.playPreviousSongSimple()
        self._setSong(songDict)

    def _setSong(self, songDict):
        songListLayout.selectAtIndex(songDict["index"])
        path = songDict["path"] + "\\" + songDict["filename"]
        self.setLoopText(songDict["loop"])
        songLayout.songInfoLayout.setNewTitle(songDict["title"])
        Player.Instance.play(path)

    def forceNextSong(self):
        if self.playlist == None:
            return
        self.playlist.setLoop(0)
        self.stopNumber -= 1
        self.nextSong()

    def forcePreviousSong(self):
        if self.playlist == None:
            return
        self.playlist.setLoop(0)
        self.stopNumber -= 1
        self.previousSong()

    def ydlHook(self, d):
        QApplication.processEvents()
        if d["status"] == "downloading":
            self.setWindowTitle(
                config.window["title_downloading"] + " - " + d["_percent_str"])
        else:
            self.setWindowTitle(config.window["title"])


mainWindow = MainWindow()
mainWindow.show()

Ydl.hook = mainWindow.ydlHook


@ Player.Instance.event_callback("end-file")
def nextSong(event):
    if mainWindow.stopNumber <= 0:
        mainWindow.stopNumber = 1
        return
    mainWindow.nextSong()


@Player.Instance.property_observer("duration")
def duration_observer(_name, duration):
    if type(duration) is float:
        songLayout.songDurationLayout.setNewDuration(int(duration))
        songLayout.songSliderLayout.setNewMax(int(duration))


@Player.Instance.property_observer("time-pos")
def time_observer(_name, time):
    if type(time) is float:
        if songLayout.songDurationLayout._time != int(time):
            songLayout.songDurationLayout.setNewTime(int(time))
            songLayout.songSliderLayout.setNewValue(int(time))


app.exec_()
