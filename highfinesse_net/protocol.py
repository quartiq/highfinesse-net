import logging
import asyncio

logger = logging.getLogger(__name__)


class HighFinesseError(Exception):
    pass


class Protocol:
    """Protocol for the HighFinesse Wavemeter"""

    def _writeline(self, line):
        raise NotImplementedError

    async def _read(self, n):
        raise NotImplementedError

    async def _readline(self):
        raise NotImplementedError

    def do(self, cmd):
        logger.debug("do %s", cmd)
        self._writeline(cmd)

    async def ask(self, cmd, *args):
        if args:
            cmd = "{} {}".format(
                cmd, ",".join(str(_) for _ in args))
        self.do(cmd)
        ret = await self._readline()
        logger.debug("ret %s", ret)
        return ret

    async def read(self, n):
        ret = await self._read(n)
        return ret.decode()

    async def ask_check(self, cmd):
        ret = await self.ask(cmd)
        if int(ret) != 0:
            raise HighFinesseError(ret)

    async def is_started(self):
        """"""
        return int(await self.ask_check("isStarted")) == 0

    async def start_device(self):
        """"""
        await self.ask_check("startDevice")

    async def close_device(self):
        """"""
        await self.ask_check("closeDevice")

    async def get_temperature(self):
        """"""
        return float(await self.ask("getTemperature"))

    async def get_pressure(self):
        """"""
        return float(await self.ask("getPressure"))

    async def get_version(self):
        """
        "Device Type <int>,
        Version Nr. <int>,
        revision Nr. <int>,
        Software Nr. <int>"
        """
        self.do("getVersion")
        ret = []
        for i in range(4):
            ret.append(await self._readline())
        return ret
        #int(_) for _ in (await self.ask("getVersion")).split(",")]

    async def ping(self):
        try:
            await self.get_version()
        except asyncio.CancelledError:
            raise
        except:
            logger.warning("ping failed", exc_info=True)
            return False
        return True

    async def get_calibration_wavelength(self, mode):
        """
        x: 0 || 1
        x = 0 :function returns the result of calibration laser before
            the last calibration;
        x=1: the result of the same signal is returned concerning the
            calibration effect
        """
        return float(await self.ask("getCalibrationWavelength", mode))

    async def get_frequency_num(self, channel):
        """channel: 1-8"""
        return float(await self.ask("getFrequencyNum", channel))

    async def get_wavelength_num(self, channel):
        """channel: 1-8"""
        return float(await self.ask("getWavelengthNum", channel))

    async def set_exposure_num(self, channel):
        """channel: 1-8"""
        return int(await self.ask("getExposureNum", channel))

    async def get_exposure_num(self, channel, ccd):
        """x: channel (1-8)
        y: CCD-Array (1-2)
        """
        return int(await self.ask("getExposureNum", channel, ccd))

    async def set_auto_exposure_num(self, channel, enable):
        """channel: 1-8"""
        return int(await self.ask("setAutoExposureNum", channel, enable))

    async def set_switch_mode(self, enable):
        """channel: 1-8"""
        return int(await self.ask("setSwitchMode", enable))

    async def get_switch_mode(self):
        """"""
        return int(await self.ask("setSwitchMode"))

    async def get_channel_count(self):
        """"""
        return int(await self.ask("getChannelCount"))

    async def get_active_channel(self):
        """"""
        return int(await self.ask("setActiveChannel"))

    async def set_active_channel(self, channel):
        """channel: 1-8"""
        return int(await self.ask("setActiveChannel", channel))

    async def set_auto_cal_mode(self, enable):
        """"""
        return int(await self.ask("setAutoCalMode", enable))

    async def get_auto_cal_mode(self):
        """"""
        return int(await self.ask("getAutoCalMode"))

    async def calibration(self, unit, value, channel):
        """unit:<long>, value: <double>, channel: <long>
        units: physical interpretation
        of calibration value:
        use:
        0 for wavelength(vac.)
        1 for wavelength(air)
        2 for frequency
        3 for wavenumber
        4 photon energy
        """
        return int(await self.ask("calibration", unit, value, channel))

    async def set_deviation_mode(self, enable):
        """"""
        return int(await self.ask("setDeviationMode", enable))

    async def get_deviation_mode(self):
        """"""
        return int(await self.ask("getDeviationMode"))

    async def set_pid_course_num(self, channel, wavelength):
        """channel: 1-8"""
        return int(await self.ask("setPidCourseNum", channel, wavelength))

    async def get_pid_course_num(self, channel):
        """channel: 1-8"""
        return float(await self.ask("getPidCourseNum", channel))
