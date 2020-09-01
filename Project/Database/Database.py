import sqlite3
from pathlib import Path

dbPath = str(Path.home()) + "/Music/pls.db"


class PlaylistDatabase():
    def __init__(self):
        with sqlite3.connect(dbPath) as conn:
            c = conn.cursor()
            c.execute(
                "CREATE TABLE IF NOT EXISTS Playlists(id INTEGER PRIMARY KEY, name TEXT NOT NULL, link TEXT NOT NULL UNIQUE)")
            conn.commit()

    def addPlaylist(self, name, link):
        with sqlite3.connect(dbPath) as conn:
            try:
                playlist = [(name, link)]
                c = conn.cursor()
                c.executemany(
                    "INSERT INTO Playlists (name, link) VALUES (?,?)", playlist)
                conn.commit()
            except:
                pass

    def removePlaylist(self, link):
        with sqlite3.connect(dbPath) as conn:
            try:
                c = conn.cursor()
                c.execute("DELETE FROM Playlists WHERE link=?", (link,))
                conn.commit()
            except:
                pass

    def getPlaylists(self):
        with sqlite3.connect(dbPath) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Playlists")
            return c.fetchall()


PlaylistDatabase = PlaylistDatabase()
