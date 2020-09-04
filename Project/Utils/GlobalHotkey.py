from pynput import keyboard
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class GlobalHotkeySignals(QObject):
    changePlayState = Signal()


class GlobalHotkey(QRunnable):
    def __init__(self):
        super(GlobalHotkey, self).__init__()
        self.signals = GlobalHotkeySignals()

    @Slot()
    def run(self):
        with keyboard.GlobalHotKeys({"<media_play_pause>": self.signals.changePlayState.emit}) as h:
            h.join()
