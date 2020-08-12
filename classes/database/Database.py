import sqlite3


class PlaylistDatabase():
    def __init__(self):
        with sqlite3.connect("pls.db") as conn:
            c = conn.cursor()
            c.execute(
                "CREATE TABLE IF NOT EXISTS Playlists(id INTEGER PRIMARY KEY, name TEXT NOT NULL, link TEXT NOT NULL UNIQUE)")
            conn.commit()

    def addPlaylist(self, name, link):
        with sqlite3.connect("pls.db") as conn:
            try:
                playlist = [(name, link)]
                c = conn.cursor()
                c.executemany(
                    "INSERT INTO Playlists (name, link) VALUES (?,?)", playlist)
                conn.commit()
                return True
            except:
                return False

    def getPlaylists(self):
        with sqlite3.connect("pls.db") as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Playlists")
            return c.fetchall()


PlaylistDatabase = PlaylistDatabase()
