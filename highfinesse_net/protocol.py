import logging
import asyncio

logger = logging.getLogger(__name__)


class Protocol:
    """Protocol for the HighFinesse Wavemeter"""

    def do(self, cmd):
        logger.debug("do %s", cmd)
        self._writeline(cmd)

    async def ask(self, cmd):
        ret = await self._readline()
        logger.debug("ret %s", ret)
        return ret

    async def read(self, n):
        ret = await self._read(n)
        return ret.decode()

    async def version(self):
        """Return the hardware/firmware version.

        Returns:
            str: Version string.
        """
        self.do("version")
        return (await self.read(7)).strip()
