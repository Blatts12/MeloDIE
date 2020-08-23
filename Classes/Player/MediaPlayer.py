from PySide2.QtMultimedia import QMediaObject, QMediaPlayer, QMediaContent, QMediaPlaylist


class MediaPlayer(QMediaPlayer):
    def __init__(self, *args, **kwargs):
        super(MediaPlayer, self).__init__(*args, **kwargs)
