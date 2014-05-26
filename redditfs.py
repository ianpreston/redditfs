import fuse
import errno
import stat
import time
import sys
import urlparse
import collections
import requests
import os
import os.path
from fsfile import *


class RedditFS(fuse.Operations):
    PERMS = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
    DIR_PERMS = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

    def __init__(self):
        self.fd = 0
        self.fs = FSDirectory('/', RedditFS.PERMS | RedditFS.DIR_PERMS, time.time())

    @property
    def dirlist(self):
        if not self._dirlist:
            self._dirlist = self._populate_dirlist()
        return self._dirlist

    def open(self, path, flags):
        self.fd += 1
        return self.fd

    def getattr(self, path, fh=None):
        f = self._traverse(path)

        if f is None:
            raise fuse.FuseOSError(errno.ENOENT)

        return f.getattr()

    def read(self, path, size, offset, fh):
        f = self._traverse(path)
        if f is None:
            raise fuse.FuseOSError(errno.ENOENT)
        if f.dir():
            raise fuse.FuseOSError(errno.EISDIR)

        return f.read(size, offset)

    def readdir(self, path, fh):
        f = self._traverse(path)
        if f is None:
            raise fuse.FuseOSError(errno.ENOENT)
        if not f.dir():
            raise fuse.FuseOSError(errno.ENOTDIR)

        return f.readdir()

    def _traverse(self, path, parent=None):
        if isinstance(path, basestring):
            # Shortcut so we don't have to call _split_path() on every
            # _traverse() call
            path = self._split_path(path)
        if parent is None:
            parent = self.fs

        if len(path) == 0:
            return parent

        fn = path.pop(0)
        node = parent.get_child(fn)

        if node is None and parent == self.fs:
            # Node is a direct descendant of the filesystem root. All direct
            # descendants are subreddits, so populate this subreddit lazily
            return self._populate_subreddit(fn)

        if node and not node.dir():
            # We've reached a leaf, cannot traverse any further
            return None

        return self._traverse(path, node)

    def _split_path(self, path):
        # TODO Move to a util module ?
        head, tail = os.path.split(path)
        if head == '' or head == os.sep:
            return [tail]
        return self._split_path(head) + [tail]
     
    def _populate_subreddit(self, subreddit):
        # TODO Some sort of cache invalidation
        r = requests.get(
            'http://api.reddit.com/r/{}/hot'.format(subreddit),
            headers={
                'User-Agent': 'redditfs /u/evilyomiel'
            },
        )
        if r.status_code == 404:
            return
        r.raise_for_status()

        links = [link['data'] for link in r.json()['data']['children']]

        root_file = FSDirectory(
            filename=subreddit,
            mode=RedditFS.PERMS | RedditFS.PERMS,
            ctime=time.time(),
        )

        for zelda in links:
            self._add_reddit_link_to_fs(root_file, zelda)
        self.fs.add_child(root_file)

        return root_file

    def _add_reddit_link_to_fs(self, fs, zelda):
        title    = zelda['title']
        filename = self._sanitize_path(title)

        permalink = urlparse.urljoin(
            'http://www.reddit.com/',
            zelda['permalink']
        )
        url = zelda['url']
        selftext = zelda['selftext']

        root_file = FSDirectory(
            filename=filename,
            mode=RedditFS.PERMS | RedditFS.DIR_PERMS,
            ctime=zelda['created_utc'],
        )

        permalink_file = FSFile(
            filename='permalink',
            mode=RedditFS.PERMS,
            content=permalink,
            ctime=zelda['created_utc'],
        )

        url_file = FSFile(
            filename='url',
            mode=RedditFS.PERMS,
            content=url,
            ctime=zelda['created_utc'],
        )

        selftext_file = FSFile(
            filename='selftext',
            mode=RedditFS.PERMS,
            content=selftext,
            ctime=zelda['created_utc'],
        )

        for f in (permalink_file, url_file, selftext_file):
            root_file.add_child(f)
        fs.add_child(root_file)

    def _sanitize_path(self, path):
        replace = (
            ('/', ''),
            (' ', '_'),
            ("'", ''),
            ('"', ''),
        )
        for r in replace:
            path = path.replace(*r)
        return path.lower()


def main():
    fuse.FUSE(RedditFS(), sys.argv[1], foreground=True)


if __name__ == '__main__':
    main()
