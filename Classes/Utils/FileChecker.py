import glob


class FlieChecker():
    def __init__(self):
        pass

    def getFile(self, path):
        return glob.glob(path + ".*")
