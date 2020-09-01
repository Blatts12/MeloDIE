from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from ..Database.Database import PlaylistDatabase


class PlaylistItem(QListWidgetItem):
    def __init__(self, playlist, listWidget, *args, **kwargs):
        self.playlist = playlist
        super(PlaylistItem, self).__init__(playlist[1], listWidget)

    def selectPlaylist(self):
        self.setText("[ " + self.playlist[1] + " ]")

    def deselectPlaylist(self):
        self.setText(self.playlist[1])


class PlaylistListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super(PlaylistListWidget, self).__init__(*args, **kwargs)
        font = self.font()
        font.setPixelSize(18)
        self.setFont(font)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("""
            QListWidget {
                background-color: #512C73;
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }

            QListWidget::item:selected {
                background-color: #422559;
                color: white;
                border-top: 1px solid rgba(255, 255, 255, 0.15);
                border-bottom: 1px solid rgba(255, 255, 255, 0.15);
            }
            QScrollBar:horizontal {
                background: #512C73;
                height: 8px;
            }

            QScrollBar:vertical {
                background: #512C73;
                width: 8px;
            }

            QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
                background: #230339;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                border: none;
            }
        """)


class PlaylistListLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(PlaylistListLayout, self).__init__(*args, **kwargs)
        self.listWidget = PlaylistListWidget()
        self.playlists = PlaylistDatabase.getPlaylists()
        for playlist in self.playlists:
            PlaylistItem(playlist, self.listWidget)

        self.indexSelected = -1
        self.indexHighlighted = 0
        self.indexLimit = len(self.playlists)
        self.listWidget.setCurrentRow(self.indexHighlighted)
        self.addWidget(self.listWidget)

    def updatePlaylists(self, previousPlaylist):
        self.listWidget.clear()
        self.playlists = PlaylistDatabase.getPlaylists()

        if (previousPlaylist == None):
            for playlist in self.playlists:
                PlaylistItem(playlist, self.listWidget)
        else:
            indexTemp = 0
            for playlist in self.playlists:
                PlaylistItem(playlist, self.listWidget)
                if (playlist[2] == previousPlaylist.link):
                    self.indexSelected = indexTemp
                    self.listWidget.item(self.indexSelected).selectPlaylist()
                indexTemp += 1
        self.indexLimit = len(self.playlists)

    def highlightNext(self):
        nextIndex = self.indexHighlighted + 1
        if nextIndex >= self.indexLimit:
            nextIndex = 0
        self.indexHighlighted = nextIndex

        self.listWidget.setCurrentRow(self.indexHighlighted)

    def highlightPrevious(self):
        nextIndex = self.indexHighlighted - 1
        if nextIndex < 0:
            nextIndex = self.indexLimit - 1
        self.indexHighlighted = nextIndex

        self.listWidget.setCurrentRow(self.indexHighlighted)

    def selectHighlighted(self):
        if self.indexSelected == self.indexHighlighted:
            return None

        if self.indexSelected != -1:
            self.listWidget.item(self.indexSelected).deselectPlaylist()

        self.indexSelected = self.indexHighlighted
        self.listWidget.item(self.indexSelected).selectPlaylist()

        return self.listWidget.item(self.indexSelected).playlist

    def getHighlighted(self):
        if self.indexLimit <= 0:
            return None

        return self.listWidget.item(self.indexHighlighted).playlist
