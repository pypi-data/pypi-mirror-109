"""Declares :class:`LocalDiskBackend`."""
import io
import os
import shutil

try:
    import aiofiles
    INSTALLED = True
except ImportError: # pragma: no cover
    INSTALLED = False

from .base import BaseStorageBackend


class LocalDiskBackend(BaseStorageBackend):
    """A :class:`~unimatrix.ext.blob.BaseStorageBackend` implementation
    that operates on the local disk(s).
    """
    __module__ = 'unimatrix.ext.blob'
    default_base_path = os.getcwd

    def __init__(self, *args, **kwargs):
        if not INSTALLED: # pragma: no cover
            raise ImportError(
                "Module aiofiles is not installed. Please run "
                "pip install aiofiles to use the unimatrix.ext.octet "
                "module with local storage."
            )
        super().__init__(*args, **kwargs)
        if not os.path.isabs(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)

    async def download(self, src: str, dst: str):
        """Downloads file from *absolute path* `src` to `dst` on the local
        filesystem.
        """
        shutil.copy2(src, dst)

    async  def exists_internal(self, path: str) -> bool:
        """Test whether an absolute path exists.  Returns False for broken
        symbolic links if the storage backend supports them.
        """
        return os.path.exists(path)

    async def push(self, src: str, dst: str):
        """Copies local `src` to remote `dst`.The `src` argument is either
        a string pointing to filepath on the local filesystem, a byte-sequence
        holding the contents of the source file, or a file-like object (open
        for reading).
        """
        dst = self.storage_path(dst)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        if isinstance(src, bytes):
            src = io.BytesIO(src)
        if hasattr(src, 'read'): # is a file like object.
            p = src.tell()
            src.seek(0)
            try:
                async with aiofiles.open(dst, 'wb') as f:
                    while True:
                        buf = src.read(1024)
                        if not buf:
                            break
                        await f.write(buf)
            finally:
                src.seek(p)
            return
        shutil.copy2(src, dst)
