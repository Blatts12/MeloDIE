from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class SongItem(QListWidgetItem):
    def __init__(self, songName, listWidget, *args, **kwargs):
        super(SongItem, self).__init__(songName, listWidget)
        self.songName = songName
        self.labelText = songName
        self.downloadLabel = ""

    def select(self):
        self.labelText = "[ " + self.songName + " ]"
        self.setText(self.downloadLabel + self.labelText)

    def deselect(self):
        self.labelText = self.songName
        self.setText(self.downloadLabel + self.labelText)

    def downloadProgress(self, percent):
        try:
            self.downloadLabel = "{" + percent.strip() + "} "
            self.setText(self.downloadLabel + self.labelText)
        except RuntimeError:
            pass

    def downloadComplete(self):
        try:
            self.downloadLabel = ""
            self.setText(self.downloadLabel + self.labelText)
        except RuntimeError:
            pass


class SongListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super(SongListWidget, self).__init__(*args, **kwargs)
        font = self.font()
        font.setPixelSize(12)
        self.setFont(font)
        self.setFocusPolicy(Qt.NoFocus)


class SongListLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super(SongListLayout, self).__init__(*args, **kwargs)
        self.listWidget = SongListWidget()
        self.indexHighlighted = 0
        self.indexSelected = -1
        self.indexLimit = -1
        self.addWidget(self.listWidget)

    def setSongList(self, songs):
        self.listWidget.clear()
        self.indexHighlighted = 0
        self.indexSelected = -1
        self.indexLimit = len(songs)
        for song in songs:
            SongItem(song.name, self.listWidget)
        self.listWidget.setCurrentRow(self.indexHighlighted)

    def highlightNext(self):
        if self.indexLimit == -1:
            return

        nextIndex = self.indexHighlighted + 1
        if nextIndex >= self.indexLimit:
            nextIndex = 0

        self.indexHighlighted = nextIndex
        self.listWidget.setCurrentRow(self.indexHighlighted)

    def highlightPrevious(self):
        if self.indexLimit == -1:
            return

        nextIndex = self.indexHighlighted - 1
        if nextIndex < 0:
            nextIndex = self.indexLimit - 1

        self.indexHighlighted = nextIndex
        self.listWidget.setCurrentRow(self.indexHighlighted)

    def selectHighlighted(self):
        if self.indexLimit == -1 or self.indexSelected == self.indexHighlighted:
            return

        if self.indexSelected != -1:
            self.listWidget.item(self.indexSelected).deselect()

        self.indexSelected = self.indexHighlighted
        self.listWidget.item(self.indexSelected).select()

        return self.indexSelected, self.listWidget.item(self.indexSelected)

    def selectAtIndex(self, index):
        if self.indexLimit == -1:
            return

        if self.indexSelected != -1:
            self.listWidget.item(self.indexSelected).deselect()

        self.indexSelected = index
        self.indexHighlighted = index
        self.listWidget.setCurrentRow(index)
        self.listWidget.item(self.indexSelected).select()

        return self.listWidget.item(self.indexSelected)
