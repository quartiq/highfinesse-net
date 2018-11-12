import time
import logging
import asyncio
import timeit

from highfinesse_net import Wavemeter


async def test(dev):
    print(dev)
    print(await dev.start_device())
    print(await dev.get_version())
    print(await dev.get_temperature())
    print(await dev.get_pressure())
    print(await dev.get_calibration_wavelength(0))
    print(await dev.get_calibration_wavelength(1))
    print(await dev.get_channel_count())
    print(await dev.get_deviation_mode())
    print(await dev.get_auto_cal_mode())
    for i in range(await dev.get_channel_count()):
        print(await dev.get_wavelength_num(i))
        print(await dev.get_exposure_num(i, 0))
        print(await dev.get_exposure_num(i, 1))

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
