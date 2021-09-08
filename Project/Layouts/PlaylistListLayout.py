from PySide2.QtWidgets import QListWidgetItem, QListWidget, QVBoxLayout
from PySide2.QtCore import Qt
from ..Database.Database import PlaylistDb


class PlaylistItem(QListWidgetItem):
    def __init__(self, playlist, listWidget):
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


class PlaylistListLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(PlaylistListLayout, self).__init__(*args, **kwargs)
        self.listWidget = PlaylistListWidget()
        self.playlists = PlaylistDb.getPlaylists()
        for playlist in self.playlists:
            PlaylistItem(playlist, self.listWidget)

        self.indexSelected = -1
        self.indexHighlighted = 0
        self.indexLimit = len(self.playlists)
        self.listWidget.setCurrentRow(self.indexHighlighted)
        self.addWidget(self.listWidget)

    def updatePlaylists(self, previousPlaylist):
        self.listWidget.clear()
        self.playlists = PlaylistDb.getPlaylists()

        if previousPlaylist is None:
            for playlist in self.playlists:
                PlaylistItem(playlist, self.listWidget)
        else:
            indexTemp = 0
            for playlist in self.playlists:
                PlaylistItem(playlist, self.listWidget)
                if playlist[2] == previousPlaylist.link:
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
        if self.indexSelected == self.indexHighlighted or self.indexLimit == 0:
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
