import sys
from PySide2.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PySide2.QtGui import QIcon
from PySide2.QtCore import QRect, QMargins, Qt
from classes.layout.MainLayout import MainLayout
from classes.layout.PlaylistListLayout import PlaylistListLayout
from classes.layout.SongListLayout import SongListLayout
from classes.base.Playlist import Playlist
from classes.base.Player import Player
from classes.base.Youtubedl import Ydl
from classes import config

app = QApplication(sys.argv)


mainLayout = MainLayout()
playlistListLayout = PlaylistListLayout()
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
        #mainLayout.addLayout(songLayout, 0, 1)
        mainLayout.addLayout(songListLayout, 0, 2)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def keyPressEvent(self, event):
        # Playlist List
        if event.key() == Qt.Key_Period:  # highlight next playlist
            playlistListLayout.highlightNext()

        elif event.key() == Qt.Key_Comma:  # highlight prev song
            playlistListLayout.highlightPrevious()

        elif event.key() == Qt.Key_Slash:  # select highlighted playlist
            playlist = playlistListLayout.selectHighlighted()
            if playlist == None:
                return
            self.playlist = Playlist(
                playlist[1], playlist[2], prepareInfo=True)
            songListLayout.setSongList(self.playlist.songs)
            self.stopNumber -= 1
            self.nextSong()

        # Song List
        elif event.key() == Qt.Key_Semicolon:  # highlight next song
            songListLayout.highlightNext()

        elif event.key() == Qt.Key_L:  # highlight prev song
            songListLayout.highlightPrevious()

        elif event.key() == Qt.Key_Apostrophe:  # select highlighted song
            index = songListLayout.selectHighlighted()
            if index == None:
                return
            self.stopNumber -= 1
            songDict = self.playlist.playSongAtIndex(index)
            path = songDict["path"] + "\\" + songDict["filename"]
            Player.Instance.play(path)

        elif event.key() == Qt.Key_S:  # shuffle
            self.playlist.shuffle()
            songListLayout.setSongList(self.playlist.songs)
            self.stopNumber -= 1
            self.nextSong()

    def nextSong(self):
        songDict = mainWindow.playlist.playNextSong()
        songListLayout.selectAtIndex(songDict["index"])
        path = songDict["path"] + "\\" + songDict["filename"]
        Player.Instance.play(path)

    def ydlHook(self, d):
        if d["status"] == "downloading":
            self.setWindowTitle(
                config.window["title_downloading"] + " - " + d["_percent_str"])
        elif d["status"] == "finished":
            self.setWindowTitle(config.window["title"])


mainWindow = MainWindow()
mainWindow.show()

Ydl.hook = mainWindow.ydlHook


@Player.Instance.event_callback("end-file")
def nextSong(event):
    if mainWindow.stopNumber == 0:
        mainWindow.stopNumber = 1
        return
    mainWindow.nextSong()


app.exec_()
