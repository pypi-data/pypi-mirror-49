from __future__ import print_function, division, absolute_import

from io import BytesIO
from fsspec import AbstractFileSystem
import logging
logger = logging.Logger('fsspec.memoryfs')


class MemoryFileSystem(AbstractFileSystem):
    """A filesystem based on a dict of BytesIO objects"""
    store = {}  # global

    def ls(self, path, detail=False):
        if path in self.store:
            # there is a key with this exact name, but could also be directory
            out = [{'name': path,
                    'size': self.store[path].getbuffer().nbytes,
                    'type': 'file'}]
        else:
            out = []
        path = path.strip('/')
        paths = set()
        for p in self.store:
            if '/' in p:
                root = p.rsplit('/', 1)[0]
            else:
                root = ''
            if root == path:
                out.append({'name': p,
                            'size': self.store[p].getbuffer().nbytes,
                            'type': 'file'})
            elif path and all((a == b) for a, b
                              in zip(path.split('/'), p.strip('/').split('/'))):
                # implicit directory
                ppath = '/'.join(p.split('/')[:len(path.split('/')) + 1])
                if ppath not in paths:
                    out.append({'name': ppath + '/',
                                'size': 0,
                                'type': 'directory'})
                    paths.add(ppath)
            elif all((a == b) for a, b
                     in zip(path.split('/'), [''] + p.strip('/').split('/'))):
                # root directory entry
                ppath = p.rstrip('/').split('/', 1)[0]
                if ppath not in paths:
                    out.append({'name': ppath + '/',
                                'size': 0,
                                'type': 'directory'})
                    paths.add(ppath)

        if detail:
            return out
        return sorted([f['name'] for f in out])

    def exists(self, path):
        return path in self.store

    def _open(self, path, mode='rb', **kwargs):
        """Make a file-like object

        Parameters
        ----------
        path: str
            identifier
        mode: str
            normally "rb", "wb" or "ab"
        """
        if mode in ['rb', 'ab', 'rb+']:
            if path in self.store:
                f = self.store[path]
                if mode == 'rb':
                    f.seek(0)
                else:
                    f.seek(0, 2)
                return f
            else:
                raise FileNotFoundError(path)
        if mode == 'wb':
            m = MemoryFile(self, path)
            if not self._intrans:
                m.commit()
            return m

    def copy(self, path1, path2, **kwargs):
        self.store[path2] = MemoryFile(self.store[path1].getbuffer())

    def cat(self, path):
        return self.store[path].getvalue()

    def _rm(self, path):
        del self.store[path]

    def ukey(self, path):
        return hash(self.store[path])  # internal ID of instance

    def size(self, path):
        """Size in bytes of the file at path"""
        if path not in self.store:
            raise FileNotFoundError(path)
        return self.store[path].getbuffer().nbytes


class MemoryFile(BytesIO):
    """A BytesIO which can't close and works as a context manager"""

    def __init__(self, fs, path):
        self.fs = fs
        self.path = path

    def __enter__(self):
        return self

    def close(self):
        pass

    def discard(self):
        pass

    def commit(self):
        self.fs.store[self.path] = self
