# pylint: skip-file
import unittest

from .. import local
from .base import BackendTests


class LocalDiskBackendTestCase(BackendTests):
    __test__ = True
    backend_class = local.LocalDiskBackend
