# pylint: skip-file
import os
import unittest

from .. import azure
from .base import BackendTests


class AzureStorageBackendTestCase(BackendTests):
    __test__ = True
    backend_class = azure.AzureStorageBackend

    def get_backend_kwargs(self):
        # Check if we can authenticate with Azure.
        try:
            from azure.identity.aio import DefaultAzureCredential
            from azure.storage.blob import BlobServiceClient
        except ImportError:
            raise unittest.SkipTest()
        if not os.getenv('AZURE_ACCESS_KEY')\
        and not os.getenv('AZURE_ACCESS_KEYFILE'):
            raise unittest.SkipTest()
        if os.getenv('AZURE_ACCESS_KEY'):
            access_key = os.getenv('AZURE_ACCESS_KEY')
        if os.getenv('AZURE_ACCESS_KEYFILE'):
            access_key = open(os.getenv('AZURE_ACCESS_KEYFILE')).read()
        return {
            'access_key': access_key,
            'container': 'unimatrix-blob'
        }
