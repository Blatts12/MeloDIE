import os
import youtube_dl


class FileManager():
    def __init__(self):
        pass

    def getFileList(self, path):
        files = os.listdir(path)
        return files

    def getFileExtList(self, path):
        files = self.getFileList(path)
        newFiles = [os.path.splitext(file) for file in files]
        return newFiles

    def fileAndExtFromSong(self, fileName, fileList):
        return [file[1] for file in fileList if file[0] == fileName]


Fm = FileManager()


class Filelist:
    def __init__(self, fileList):
        self.fileList = fileList

    def append(self, item):
        self.fileList.append(item)

    def getFileList(self):
        return self.fileList
