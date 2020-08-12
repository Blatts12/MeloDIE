from PySide2.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem, QWidget, QLabel
from PySide2.QtGui import QFont
from PySide2.QtCore import Qt
from .. import config


class SongItem(QListWidgetItem):
    def __init__(self, songName, listWidget, *args, **kwargs):
        self.songName = songName
        super(SongItem, self).__init__(songName, listWidget)

    def selectSong(self):
        self.setText("[ " + self.songName + " ]")

    def deselectSong(self):
        self.setText(self.songName)


class SongListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super(SongListWidget, self).__init__(*args, **kwargs)
        font = QFont()
        font.setPixelSize(12)
        self.setFont(font)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("""
            QListWidget {{
                background-color: #{w_bg}; 
                border: none;
                border-left: 1px solid rgba(255, 255, 255, 0.1);
            }}

            QListWidget::item:selected {{
                background-color: #{h_bg};
                color: white;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}

            QScrollBar:horizontal {{
                background: #{w_bg};
                height: 8px;
            }}

            QScrollBar:vertical {{
                background: #{w_bg};
                width: 8px;
            }}

            QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
                background: #{sb_bg};
            }}

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal, QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none;
                border: none;
            }}
        """.format(
            w_bg=config.colors["widget"],
            h_bg=config.colors["highlight"],
            sb_bg=config.colors["scrollbar"]
        ))


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
        if self.indexLimit == -1:
            return

        if self.indexSelected == self.indexHighlighted:
            return

        if self.indexSelected != -1:
            self.listWidget.item(self.indexSelected).deselectSong()

        self.indexSelected = self.indexHighlighted
        self.listWidget.item(self.indexSelected).selectSong()

        return self.indexSelected

    def selectAtIndex(self, index):
        if self.indexLimit == -1:
            return

        if self.indexSelected != -1:
            self.listWidget.item(self.indexSelected).deselectSong()

        self.indexSelected = index
        self.indexHighlighted = index
        self.listWidget.setCurrentRow(index)
        self.listWidget.item(self.indexSelected).selectSong()
