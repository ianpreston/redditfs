import stat
import enum


DirectoryType = enum.Enum('DirectoryType', 'root normal subreddit')


class FSFile(object):
    BASE_MODE = stat.S_IFREG

    def __init__(self, filename, mode, content, ctime):
        self.filename = filename
        self._mode    = FSFile.BASE_MODE | mode
        self._content = content.encode('ascii', errors='ignore')
        self._size    = len(self._content)
        self._time    = ctime

    def getattr(self):
        return {
            'st_size': self._size,
            'st_nlink': 1,
            'st_ctime': self._time,
            'st_mtime': self._time,
            'st_atime': self._time,
            'st_mode': self._mode,
        }

    def read(self, size, offset):
        return self._content[offset:offset+size]

    def dir(self):
        return False


class FSDirectory(object):
    BASE_MODE = stat.S_IFDIR

    def __init__(self, filename, dirtype, mode, ctime):
        self.filename  = filename
        self.dirtype   = dirtype
        self._mode     = FSDirectory.BASE_MODE | mode
        self._time     = ctime
        self._children = {}

    def add_child(self, child):
        self._children[child.filename] = child

    def get_child(self, path):
        return self._children.get(path)

    def remove_child(self, path):
        del self._children[path]

    def getattr(self):
        return {
            'st_size': 0,
            'st_nlink': len(self._children),
            'st_ctime': self._time,
            'st_mtime': self._time,
            'st_atime': self._time,
            'st_mode': self._mode,
        }

    def readdir(self):
        return ['.', '..'] + list(self._children.keys())

    def dir(self):
        return True
