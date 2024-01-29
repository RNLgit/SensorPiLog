import subprocess
from datetime import datetime
from collections import namedtuple
from typing import Union

STD_P_KPA = 101.325
HUMIDITY_COMFORT = [30, 50]
STD_PRESSURE_KPA = 101.325

PiDataFormat = namedtuple(
    "PiDataFormat", ["time", "temperature", "humidity", "pressure", "accelerometer", "gyroscope", "compass", "cpu_temp"]
)


def is_raspberry_pi():
    try:
        with open("/proc/device-tree/model") as f:
            return "Raspberry Pi" in f.read()
    except Exception:
        return False


if is_raspberry_pi():
    from sense_hat import SenseHat
else:
    print("Not running on Raspberry Pi, PiSensor for sense hat will not work.")


class PiSensor(object):
    def __init__(self):
        self.sense = SenseHat()

    @staticmethod
    def get_cpu_temp() -> Union[float, None]:
        """
        get current RPI cpu temperature
        Unit in deg C
        :param round_to: round result to decimal points
        """
        process = subprocess.Popen(["vcgencmd", "measure_temp"], stdout=subprocess.PIPE)
        output, error = process.communicate()
        if not error:
            return float(output.decode("ascii")[5:-3])  # e.g. reading: temp=42.3'C
        else:
            return None

    def get_temperature(self, round_to=2) -> float:
        """
        get Sense hat on board temperature sensor reading, in deg C
        """
        return round(float(self.sense.get_temperature()), round_to)

    def get_humidity(self, round_to=1) -> float:
        """
        get Sense hat humidity sensor reading, in % relative humidity
        """
        return round(float(self.sense.get_humidity()), round_to)

    def get_pressure_kpa(self, round_to=3) -> float:
        """
        get sense hat temperature reading, in KPa
        """
        return round(self.sense.get_pressure() * 0.1, round_to)

    @staticmethod
    def get_today() -> str:
        """
        get current timer reading month stamp. e.g. Dec 2020: 2020-12-11
        """
        return datetime.today().strftime("%Y-%m-%d")

    @staticmethod
    def get_time() -> str:
        """
        get current data time timestamp. e.g. 20:13:52, 04 Sep 2019 will be: 2019-09-04-20-13-52
        """
        return datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def read_all(self) -> PiDataFormat:
        """
        get a namedtuple of sense hat supported data (and CPU reading) readings including local time and rpi cpu temp
        """
        return PiDataFormat(
            time=self.get_time(),
            temperature=self.get_temperature(),
            humidity=self.get_humidity(),
            pressure=self.get_pressure_kpa(),
            accelerometer=self.sense.get_accelerometer(),
            gyroscope=self.sense.get_gyroscope(),
            compass=self.sense.get_compass(),
            cpu_temp=self.get_cpu_temp(),
        )
