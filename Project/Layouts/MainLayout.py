from PySide2.QtWidgets import QGridLayout
from PySide2.QtCore import QMargins


class MainLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        self.setColumnStretch(0, 200)
        self.setColumnStretch(1, 400)
        self.setColumnStretch(2, 200)
        self.setContentsMargins(QMargins(0, 0, 0, 0))
