import subprocess
from datetime import datetime
from sense_hat import SenseHat
from os import path

sense = SenseHat()

STD_P_KPA = 101.325
HUMIDITY_COMFORT = [30, 50]
STD_PRESSURE_KPA = 101.325


class Sensor(object):
    DATA_SEPARATOR = ','

    @staticmethod
    def get_cpu_temp(round_to=2) -> float:
        """
        get current RPI cpu temperature
        :param round_to: round result to decimal points
        """
        result = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
        result = result.stdout.read().decode('ascii')
        temp = result.split('=')[1][0:4]  # will get temp=52^C
        return round(float(temp), round_to)

    @staticmethod
    def get_temperature(round_to=2) -> float:
        return round(float(sense.get_temperature()), round_to)

    @staticmethod
    def get_humidity(round_to=1) -> float:
        return round(float(sense.get_humidity()), round_to)

    @staticmethod
    def get_pressure_delta(round_to=3) -> float:
        return round(sense.get_pressure() * 0.1 - STD_PRESSURE_KPA, round_to)

    @staticmethod
    def get_month_stamp() -> str:
        return datetime.today().strftime('%Y-%m')

    @staticmethod
    def get_timestamp() -> str:
        return datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

    @classmethod
    def sample_one_data(cls) -> tuple:
        return cls.get_timestamp(), cls.get_cpu_temp(), cls.get_temperature(), \
               cls.get_humidity(), cls.get_pressure_delta()

    @classmethod
    def log_one_data(cls, log_dir='/var/log', log_filename='sense.log'):
        with open(path.join(log_dir, log_filename), 'a') as f:
            f.write(cls.DATA_SEPARATOR.join(map(str, cls.sample_one_data())))


if __name__=='__main__':
    print('sensor logger starts')