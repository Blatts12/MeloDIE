from pynput import keyboard
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class GlobalHotkeySignals(QObject):
    changePlayState = Signal()
    volumeUp = Signal()
    volumeDown = Signal()
    mute = Signal()
    nextSong = Signal()
    prevSong = Signal()


class GlobalHotkey(QRunnable):
    def __init__(self):
        super(GlobalHotkey, self).__init__()
        self.signals = GlobalHotkeySignals()
        self.listener = keyboard.GlobalHotKeys({"<media_play_pause>": self.signals.changePlayState.emit,
                                                "<pause>++": self.signals.volumeUp.emit,
                                                "<pause>+-": self.signals.volumeDown.emit,
                                                "<pause>+*": self.signals.mute.emit,
                                                "<media_next>": self.signals.nextSong.emit,
                                                "<media_previous>": self.signals.prevSong.emit})

    def stop(self):
        self.listener.stop()

    @Slot()
    def run(self):
        with self.listener as l:
            l.join()
