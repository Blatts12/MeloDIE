from PySide2.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem
from PySide2.QtCore import QMargins, QModelIndex, Qt
from PySide2.QtGui import QFont
from ..database.Database import PlaylistDatabase
from .. import config


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
        font = QFont()
        font.setPixelSize(18)
        self.setFont(font)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("""
            QListWidget {{
                background-color: #{w_bg}; 
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }}

            QListWidget::item:selected {{
                background-color: #{h_bg};
                color: white;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
        """.format(
            w_bg=config.colors["widget"],
            h_bg=config.colors["highlight"]
        ))


class PlaylistListLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(PlaylistListLayout, self).__init__(*args, **kwargs)
        self.listWidget = PlaylistListWidget()
        self.playlists = PlaylistDatabase.getPlaylists()
        self.indexSelected = -1
        self.indexHighlighted = 0
        self.indexLimit = len(self.playlists)

        for playlist in self.playlists:
            PlaylistItem(playlist, self.listWidget)

        self.listWidget.setCurrentRow(self.indexHighlighted)
        self.addWidget(self.listWidget)

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
