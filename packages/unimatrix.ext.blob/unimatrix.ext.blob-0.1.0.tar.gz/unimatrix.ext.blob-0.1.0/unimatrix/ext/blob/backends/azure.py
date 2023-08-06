"""Declares :class:`AzureStorageBackend`."""
import os

try:
    from azure.core.exceptions import ResourceNotFoundError
    #from azure.identity.aio import DefaultAzureCredential
    from azure.storage.blob.aio import BlobClient
    INSTALLED = True
except ImportError: # pragma: no cover
    INSTALLED = False
import aiofiles

from .base import BaseStorageBackend


class AzureStorageBackend(BaseStorageBackend):
    """A :class:`BaseStorageBackend` implementation that uses Microsoft Azure
    Blob Storage as the underlying storage provider.

    It is recommended to set a storage retention policy on the storage container
    used with :class:`AzureStorageBackend`. The implementation relies on
    soft deletes being available (i.e. ``BlobClient.undelete_blob()``).
    """
    __module__ = 'unimatrix.ext.blob'
    default_base_path: str = ''
    absolute_base_path: bool = False

    #: The URL of the Microsoft Azure storage account
    account_url: str = None

    def __init__(self,
        container,
        account: str = None,
        access_key: str = None,
        base_path: str = None
    ):
        """Initialize a new :class:`AzureStorageBackend` instance."""
        if not INSTALLED: # pragma: no cover
            raise ImportError(
                "Either Module azure-storage-blob or azure-identity is not "
                "installed. Please run pip install azure_storage_blob "
                "azure-identity to use the unimatrix.ext.octet module with "
                "Microsoft Azure."
            )
        super().__init__(base_path)
        #if account:
        #    self.account_url = f'https://{account}.blob.core.windows.net'
        self.access_key = access_key
        self.container = container
        if not self.account_url and not self.access_key: # pragma: no cover
            raise TypeError("Specify either account_url or access_key.")

    async def download(self, src: str, dst: str):
        """Downloads file from *absolute path* `src` to `dst` on the local
        filesystem.
        """
        blob = self.get_blob_client(src)
        downloader = await blob.download_blob()
        async with aiofiles.open(dst, 'wb') as f:
            async for chunk in downloader.chunks():
                await f.write(chunk)

    async def exists_internal(self, path: str) -> bool:
        """Test whether an absolute path exists.  Returns False for broken
        symbolic links if the storage backend supports them.
        """
        blob = self.get_blob_client(path)
        return await blob.exists()

    async def upload(self, src: str, dst: str):
        """Uploads absolute path `src` to absolute path `dst`."""
        if not os.path.exists(src) or not os.path.isfile(src): # pragma: no cover
            raise FileNotFoundError(f"No such file: {src}")
        blob = self.get_blob_client(dst)
        is_new = await blob.exists()
        must_undelete = False
        if not is_new:
            try:
                await blob.delete_blob()
                must_undelete = True # pragma: no cover
            except ResourceNotFoundError:
                pass
        try:
            await blob.create_append_blob()
            async with aiofiles.open(src, 'rb') as f:
                while True:
                    buf = await f.read()
                    if not buf:
                        break
                    await blob.append_block(buf)
        except Exception: # pragma: no cover pylint: disable=W0703
            if must_undelete:
                await blob.undelete_blob()

    def get_blob_client(self, path: str) -> BlobClient:
        """Return a :class:`azure.storage.blob.aio.BlobClient` instance
        configured for the given `path`.
        """
        params = {
            'blob_name': path,
            'container_name': self.container
        }
        if self.access_key and not self.account_url:
            # Use connection string
            return BlobClient.from_connection_string(
                conn_str=self.access_key, **params
            )

        raise NotImplementedError # pragma: no cover
        #return self._client_factory(BlobClient,
        #    account_url=self.account_url, **params
        #)

    #def _client_factory(self, cls, *args, **kwargs): # pragma: no cover
    #    return cls(credential=DefaultAzureCredential(), *args, **kwargs)
