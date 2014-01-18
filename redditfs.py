import fuse
import errno
import stat
import StringIO
import time
import sys
import urlparse
import collections
import requests


Zelda = collections.namedtuple('Zelda', ['path', 'title', 'content', 'size', 'time'])


class RedditFS(fuse.Operations):
	REDDIT = 'http://reddit.com/'
	PERMS = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
	ROOT_PERMS = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

	def __init__(self, subreddit):
		self.subreddit = subreddit
		self.fd = 0
		self._dirlist = None

	@property
	def dirlist(self):
		if not self._dirlist:
			self._dirlist = self._populate_dirlist()
		return self._dirlist

	def open(self, path, flags):
		self.fd += 1
		return self.fd

	def getattr(self, path, fh=None):
		if path == '/':
			return {
				'st_size': 0,
				'st_nlink': len(self.dirlist),
				'st_ctime': time.time(),
				'st_mtime': time.time(),
				'st_atime': time.time(),
				'st_mode': stat.S_IFDIR | RedditFS.PERMS | RedditFS.ROOT_PERMS,
			}

		zelda = self._get_zelda(path)
		if zelda == None:
			raise fuse.FuseOSError(errno.ENOENT)

		return {
			'st_size': zelda.size,
			'st_nlink': 1,
			'st_ctime': zelda.time,
			'st_mtime': zelda.time,
			'st_atime': zelda.time,
			'st_mode': stat.S_IFREG | RedditFS.PERMS,
		}			

	def read(self, path, size, offset, fh):
		zelda = self._get_zelda(path)
		if zelda == None:
			raise fuse.FuseOSError(errno.ENOENT)

		return zelda.content[offset:offset+size]

	def readdir(self, path, fh):
		return ['.', '..'] + self.dirlist.keys()

	def _populate_dirlist(self):
		# TODO Some sort of cache invalidation
		r = requests.get('http://api.reddit.com/r/{}/hot'.format(self.subreddit))
		r.raise_for_status()

		links = [self._mk_zelda(link['data']) for link in r.json()['data']['children']]
		return {l.path:l for l in links if l }

	def _mk_zelda(self, link):
		title = link['title'].encode('ascii', errors='ignore')
		permalink = urlparse.urljoin(RedditFS.REDDIT, link['permalink']).encode('ascii', errors='ignore')

		return Zelda(
			path=self._sanitize_path(title),
			title=title,
			content=permalink,
			size=len(permalink),
			time=link['created_utc'],
		)

	def _get_zelda(self, path):
		return self.dirlist.get(path[1:])

	def _sanitize_path(self, path):
		replace = (
			('/', ''),
			(' ', '_'),
			("'", ''),
			('"', ''),
			('.', ''),
			('', ''),
		)
		for r in replace:
			path = path.replace(*r)
		return path


def main():
	fuse.FUSE(RedditFS(sys.argv[2]), sys.argv[1], foreground=True)


if __name__ == '__main__':
	main()