import subprocess
import os
from datetime import datetime
from sense_hat import SenseHat
import time
from threading import Thread

sense = SenseHat()

std_p_kpa = 101.325
humidity_comfort = [30, 50]
std_pressure_kpa = 101.325


class Sensor(object):
    @staticmethod
    def get_cpu_temp(round_to=2):
        result = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
        result = result.stdout.read().decode('ascii')
        temp = result.split('=')[1][0:4]  # will get temp=52^C
        return round(float(temp), round_to)

    @staticmethod
    def get_temperature(round_to=2):
        return round(float(sense.get_temperature()), round_to)

    def get_humidity(self, round_to=1):
        return round(float(sense.get_humidity()), round_to)

    def get_pressure_delta(self, round_to=3):
        return round(sense.get_pressure() * 0.1 - std_pressure_kpa, round_to)

    def get_month_stamp(self):
        return datetime.today().strftime('%Y-%m')

    def get_timestamp(self):
        return datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

    def sample_one_data(self):
        return f'{get_timestamp()},{get_cpu_temp()},{get_temperature()},{get_humidity()},{get_pressure_delta()}\n'

    def log_one_data(self):
        with open(f'./sensor_logs/{get_month_stamp()}.txt', 'a') as f:
            f.write(sample_one_data())

    def logging(self, live=True, interval_s=600):
        while live:
            log_one_data()
            time.sleep(interval_s)


if __name__=='__main__':
    print('sensor logger starts')
    log_th = Thread(target=logging, args=())
    log_th.start()