import asyncio

from .protocol import Protocol


class TCP(Protocol):
    eol_write = b"\r\n"
    eol_read = b"\r\n"

    def __init__(self, reader, writer):
        self._reader = reader
        self._writer = writer

    @classmethod
    async def connect(cls, host, port=1234, **kwargs):
        reader, writer = await asyncio.open_connection(host, port, **kwargs)
        obj = cls(reader, writer)
        if int(await obj._readline()) != 200:
            raise ValueError("did not receive `200`")
        return obj

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def close(self):
        self._writer.close()

    def _writeline(self, cmd):
        self._writer.write(cmd.encode() + self.eol_write)

    async def _readline(self):
        r = await self._reader.readline()
        if not r.endswith(self.eol_read):
            raise ValueError("eol not found in response", r)
        return r[:-len(self.eol_read)].decode()

    async def _read(self, n):
        return await self._reader.read(n)
