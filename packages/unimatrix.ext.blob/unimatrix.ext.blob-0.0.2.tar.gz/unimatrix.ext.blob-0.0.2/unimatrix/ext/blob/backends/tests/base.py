# pylint: skip-file
import io
import tempfile
import os
import unittest

import aiofiles
import pytest


class BackendTests:
    __test__ = False

    @pytest.fixture
    def backend(self):
        return self.get_backend()

    def get_backend(self):
        return self.backend_class(**self.get_backend_kwargs())

    def get_backend_kwargs(self):
        return {
            'base_path': tempfile.mkdtemp()
        }

    @pytest.mark.asyncio
    async def test_push_creates_file(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_from_filelike(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        f = io.BytesIO(buf)
        await backend.push(f, dst)
        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_from_bytes(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        await backend.push(buf, dst)
        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_with_path(self, backend):
        dst = f'{bytes.hex(os.urandom(16))}/foo/bar/baz'
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        assert await backend.exists(dst)

    @pytest.mark.asyncio
    async def test_push_pull_is_equal(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_pull_is_equal_with_path(self, backend):
        dst = f'{bytes.hex(os.urandom(16))}/foo'
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc
