import time
import logging
import asyncio
import timeit

from highfinesse_net import Wavemeter


async def test(dev):
    print(dev)
    print(await dev.status())
    print(await dev.version())

def main():
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    # loop.set_debug(False)
    async def run():
        with await Wavemeter.connect("schumi") as dev:
            await test(dev)
    loop.run_until_complete(run())


if __name__ == "__main__":
    main()
