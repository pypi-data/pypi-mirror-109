"""Declares :class:`IStorageBackend`."""


class IStorageBackend:
    """Specifies the interface that storage backend implementations must
    implement.
    """
    __module__ = 'unimatrix.ext.blob'

    async def download(self, src: str, dst: str):
        """Downloads file from *absolute path* `src` to `dst` on the local
        filesystem.
        """
        raise NotImplementedError("Subclasses must override this method.")

    async  def exists_internal(self, path: str) -> bool:
        """Test whether an absolute path exists.  Returns False for broken
        symbolic links if the storage backend supports them.
        """
        raise NotImplementedError("Subclasses must override this method.")

    async def push(self, src: object, dst: str):
        """Copies local `src` to remote `dst`.The `src` argument is either
        a string pointing to filepath on the local filesystem, a byte-sequence
        holding the contents of the source file, or a file-like object (open
        for reading).
        """
        raise NotImplementedError("Subclasses must override this method.")
