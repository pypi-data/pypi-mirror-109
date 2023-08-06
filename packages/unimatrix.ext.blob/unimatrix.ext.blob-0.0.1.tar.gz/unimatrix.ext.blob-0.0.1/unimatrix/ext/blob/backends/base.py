"""Declares :class:`BaseStorageBackend`."""
import os
import tempfile

from .istoragebackend import IStorageBackend


class BaseStorageBackend(IStorageBackend):
    """The base class for all storage backends."""
    __module__ = 'unimatrix.ext.blob'

    #: Specifies the capabilities of the backend.
    capabilities: list = []

    #: Specifies the supported write modes by a :class:`BaseStorageBackend`
    #: implementation.
    write_modes: list = ['w', 'wt', 'wb']

    #: Specifies the supported read modes by a :class:`BaseStorageBackend`
    #: implementation.
    read_modes: list = ['r', 'rt', 'rb']

    #: Indicates the default base path for this storage backend. If this
    #: attribute is ``None``, then the ``base_path`` parameter is mandatory
    #: when creating a new instance.
    default_base_path = None

    def __init__(self, base_path=None):
        """Initialize the storage backend.

        Args:
            base_path (str): the base path that the storage backend writes
                all files relative to. If `base_path` is ``None``, then
                :attr:`default_base_path` is used.
        """
        if base_path is None: # pragma: no cover
            self.base_path = self.default_base_path\
                if not callable(self.default_base_path)\
                else self.default_base_path()
        else:
            self.base_path = base_path
        if self.base_path is None: # pragma: no cover
            raise TypeError(
                "The `base_path` argument was not provided and "
                "no default was set for storage backend implementation"
                f" {type(self).__name__}"
            )

    async def exists(self, path: str) -> bool:
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return await self.exists_internal(self.storage_path(path))

    async def pull(self, src: str, dst: str = None) -> str:
        """Pulls a file from the given `src` in the storage backend to local
        filepath `dst`. If `dst` is ``None``, then a temporary filepath is
        generated.
        """
        if dst is None:
            _, dst = tempfile.mkstemp()
        await self.download(self.storage_path(src), dst)
        return dst

    #def open(self, path: str, mode='rt', *args, **kwargs): # pylint: disable=W1113
    #    """Open the given `path` in the given `mode`."""
    #    if mode not in set(self.write_modes + self.read_modes): # pragma: no cover
    #        raise NotImplementedError(f"Unsupported mode: {mode}")
    #    return self.descriptor_class(self, path, mode, *args, **kwargs)

    def storage_path(self, *components):
        """Returns the absolute path in the storage of `path`."""
        return os.path.join(self.base_path or '', *components)
