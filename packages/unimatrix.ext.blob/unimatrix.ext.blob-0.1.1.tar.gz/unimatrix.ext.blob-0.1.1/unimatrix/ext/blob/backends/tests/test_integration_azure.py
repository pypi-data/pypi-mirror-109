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
        return {
            'account': 'unimatrixtesting',
            'container': 'unimatrix-blob'
        }
