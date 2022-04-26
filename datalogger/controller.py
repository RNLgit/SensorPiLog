from RPi.GPIO import BOARD, BCM
from rpi_hardware_pwm import HardwarePWM
import adafruit_pcf8591.pcf8591 as pcf
from adafruit_pcf8591.analog_in import AnalogIn


HW_PWM_MAP = {BOARD: {12: 0, 35: 1},
              BCM: {18: 0, 19: 1}}


class Controller(object):
    def start_pwm(self, duty_cycle: int):
        raise NotImplementedError

    def set_frequency(self, frequency: int):
        raise NotImplementedError

    def set_duty_cycle(self, duty_cycle: int):
        raise NotImplementedError

    def stop_pwm(self):
        raise NotImplementedError

class NMosPWM(Controller):
    def __init__(self, pin_no, pinout_type=BOARD):
        if pin_no not in HW_PWM_MAP[pinout_type].keys():
            raise ValueError(f'')
