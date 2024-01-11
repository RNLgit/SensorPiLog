from sense_hat import SenseHat
import subprocess
from datetime import datetime
from os import path

STD_P_KPA = 101.325
HUMIDITY_COMFORT = [30, 50]
STD_PRESSURE_KPA = 101.325


class RpiSensor(object):
    DATA_SEPARATOR = ','

    def __init__(self):
        self.sense = SenseHat()

    @staticmethod
    def get_cpu_temp() -> float:
        """
        get current RPI cpu temperature
        Unit in deg C
        :param round_to: round result to decimal points
        """
        result = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
        return float(result.stdout.read().decode('ascii')[5:-3])  # e.g. reading: temp=42.3'C

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
        return datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def get_time() -> str:
        """
        get current data time timestamp. e.g. 20:13:52, 04 Sep 2019 will be: 2019-09-04-20-13-52
        """
        return datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

    def read_all(self) -> tuple:
        """
        get a tuple of sense hat supported data (and CPU reading) readings
        :return: exact date time seconds, cpu temperature, sense hat board temperature,
            relative humidity, atmospheric pressure
        """
        return self.get_time(), self.get_cpu_temp(), self.get_temperature(), self.get_humidity(), self.get_pressure_kpa()

    def log_one_data(self, log_dir='/var/log', log_filename='sense.log'):
        """
        Sample a group of environmental reading and log it into system log.
        :param log_dir: directory of log going to save. Default /vat/log
        :param log_filename: log filename to log data. Default sense.log
        """
        with open(path.join(log_dir, log_filename), 'a') as f:
            f.write(self.DATA_SEPARATOR.join(map(str, self.sample_one_data())))
