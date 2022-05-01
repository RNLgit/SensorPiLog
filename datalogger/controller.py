from RPi.GPIO import BOARD, BCM
from rpi_hardware_pwm import HardwarePWM


HW_PWM_MAP = {BOARD: {12: 0, 35: 1},
              BCM: {18: 0, 19: 1}}
AUDIBLE_SPECTRUM = range(20, 20_000)


class Controller(object):
    def start_pwm(self, duty_cycle: int):
        raise NotImplementedError

    def set_frequency(self, frequency: int):
        raise NotImplementedError

    def set_duty_cycle(self, duty_cycle: int):
        raise NotImplementedError

    def stop_pwm(self):
        raise NotImplementedError

    def __del__(self):
        self.stop_pwm()


class NMosPWM(Controller):
    def __init__(self, pin_no, frequency=25_000, pinout_type=BOARD):
        if pin_no not in HW_PWM_MAP[pinout_type].keys():
            raise ValueError(f'RPI pin {pin_no} not support hardware pwm')
        self.__frequency = frequency
        self.__duty_cycle = None
        self.is_stopped = True
        self.pwm = HardwarePWM(pwm_channel=HW_PWM_MAP[pinout_type][pin_no], hz=self.freq)

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.set_frequency(value)

    @property
    def duty_cycle(self):
        return self.__duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        self.set_duty_cycle(value)

    @duty_cycle.setter
    def duty_cycle(self, value):
        self.__duty_cycle = value

    def set_frequency(self, frequency: int):
        if frequency <= 0:
            raise ValueError('frequency need to be positive non-zero int')
        self.pwm.change_frequency(frequency)
        self.__frequency = frequency

    def set_duty_cycle(self, duty_cycle: int):
        if not 0 <= duty_cycle <= 100:
            raise ValueError('Duty cycle can only be non negative int from 0 to 100')
        self.pwm.change_duty_cycle(duty_cycle)
        self.__duty_cycle = duty_cycle

    def start_pwm(self, duty_cycle: int):
        if not 0 <= duty_cycle <= 100:
            raise ValueError('Duty cycle can only be non negative int from 0 to 100')
        self.pwm.start(duty_cycle)
        self.__duty_cycle = duty_cycle
        self.is_stopped = False

    def stop_pwm(self):
        self.pwm.stop()
        self.is_stopped = True
