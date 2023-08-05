import os
import shutil
import tempfile
from fsspec import AbstractFileSystem


class LocalFileSystem(AbstractFileSystem):
    """Interface to files on local storage

    Parameters
    ----------
    auto_mkdirs: bool
        Whether, when opening a file, the directory containing it should
        be created (if it doesn't already exist). This is assumed by pyarrow
        code.
    """
    root_marker = '/'

    def __init__(self, auto_mkdir=True, **kwargs):
        super().__init__(**kwargs)
        self.auto_mkdir = auto_mkdir

    def mkdir(self, path, **kwargs):
        os.mkdir(path, **kwargs)

    def makedirs(self, path, exist_ok=False):
        os.makedirs(path, exist_ok=exist_ok)

    def rmdir(self, path):
        os.rmdir(path)

    def ls(self, path, detail=False):
        paths = [os.path.abspath(os.path.join(path, f))
                 for f in os.listdir(path)]
        if detail:
            return [self.info(f) for f in paths]
        else:
            return paths

    def glob(self, path):
        path = os.path.abspath(path)
        return super().glob(path)

    def info(self, path):
        out = os.stat(path, follow_symlinks=False)
        dest = False
        if os.path.isfile(path):
            t = 'file'
        elif os.path.isdir(path):
            t = 'directory'
        elif os.path.islink(path):
            t = 'link'
            dest = os.readlink(path)
        else:
            t = 'other'
        result = {
            'name': path,
            'size': out.st_size,
            'type': t,
            'created': out.st_ctime
        }
        for field in ['mode', 'uid', 'gid', 'mtime']:
            result[field] = getattr(out, 'st_' + field)
        if dest:
            result['destination'] = dest
        return result

    def copy(self, path1, path2, **kwargs):
        """ Copy within two locations in the filesystem"""
        shutil.copyfile(path1, path2)

    get = copy
    put = copy

    def mv(self, path1, path2, **kwargs):
        """ Move file from one location to another """
        os.rename(path1, path2)

    def rm(self, path, recursive=False, maxdepth=None):
        if recursive:
            shutil.rmtree(path)
        else:
            os.remove(path)

    def _open(self, path, mode='rb', block_size=None, **kwargs):
        if self.auto_mkdir:
            self.makedirs(self._parent(path), exist_ok=True)
        return LocalFileOpener(path, mode, fs=self, **kwargs)

    def touch(self, path, **kwargs):
        """ Create empty file, or update timestamp """
        if self.exists(path):
            os.utime(path, None)
        else:
            open(path, 'a').close()


class LocalFileOpener(object):
    def __init__(self, path, mode, autocommit=True, fs=None, **kwargs):
        self.path = path
        self.fs = fs
        self.autocommit = autocommit
        if autocommit or 'w' not in mode:
            self.f = open(path, mode=mode)
        else:
            # TODO: check if path is writable?
            i, name = tempfile.mkstemp()
            self.temp = name
            self.f = open(name, mode=mode)
        if 'w' not in mode:
            self.details = self.fs.info(path)
            self.size = self.details['size']
            self.f.size = self.size

    def commit(self):
        if self.autocommit:
            raise RuntimeError('Can only commit if not already set to '
                               'autocommit')
        os.rename(self.temp, self.path)

    def discard(self):
        if self.autocommit:
            raise RuntimeError('Cannot discard if set to autocommit')
        os.remove(self.temp)

    def __fspath__(self):
        # uniquely for fsspec implementations, this is a real path
        return self.path

    def __getattr__(self, item):
        return getattr(self.f, item)

    def __enter__(self):
        self._incontext = True
        return self.f.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self._incontext = False
        self.f.__exit__(exc_type, exc_value, traceback)
