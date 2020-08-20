from __future__ import unicode_literals
import youtube_dl
import json


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass
        # print(msg)


class Youtubedl():
    def __init__(self):
        self._ydl_opts_info = {
            "format": "bestaudio/best",
            "extract_flat": True,
            "dump_single_json": True
        }
        self.path = None
        self.hook = None
        self._ydl_opts_download = {}

    def getInfoPlaylist(self, link):
        with youtube_dl.YoutubeDL(self._ydl_opts_info) as ydl:
            return ydl.extract_info(link, download=False)

    def changePlaylist(self, path):
        self.path = path

    def downloadAngGetExt(self, link, title):
        self._ydl_opts_download = {
            "format": "bestaudio/best",
            "outtmpl": self.path + "\\" + title + ".%(ext)s",
            "progress_hooks": [self.hook]
        }
        with youtube_dl.YoutubeDL(self._ydl_opts_download) as ydl:
            dict_info = ydl.extract_info(link, download=True)
            return "." + dict_info["ext"]


Ydl = Youtubedl()
