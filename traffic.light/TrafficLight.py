"""
File: TrafficLight.py
By: Gustavo Chavez
"""

from enum import Enum
import RPi.GPIO as GPIO
import time


def traffic_controller(signal_list):
    while True:
        time.sleep(5)
        for traffic_signal in signal_list:
            print(traffic_signal.status)
            traffic_signal.switch_states()


class TrafficLight:
    def __init__(self, red_value, amber_value, green_value):
        self.status = Color.DEFAULT
        self.red_light = red_value
        self.amber_light = amber_value
        self.green_light = green_value
        GPIO.setup(red_value, GPIO.OUT)
        GPIO.setup(amber_value, GPIO.OUT)
        GPIO.setup(green_value, GPIO.OUT)
        GPIO.output(self.red_light, False)
        GPIO.output(self.amber_light, False)
        GPIO.output(self.green_light, False)
        self.enable()

    def enable(self):
        if self.is_red():
            GPIO.output(self.red_light, True)
        elif self.is_amber():
            GPIO.output(self.amber_light, True)
        elif self.is_green():
            GPIO.output(self.green_light, True)
        else:
            self.disable_lights()

    def is_red(self):
        if self.status.name == 'RED':
            return True

    def is_amber(self):
        if self.status.name == 'AMBER':
            return True

    def is_green(self):
        if self.status.name == 'GREEN':
            return True

    def disable_lights(self):
        GPIO.output(self.red_light, False)
        GPIO.output(self.amber_light, False)
        GPIO.output(self.green_light, False)

    def set_status(self, color_str):
        if color_str == 'DEFAULT':
            self.status = Color.DEFAULT
        elif color_str == 'RED':
            self.status = Color.RED
        elif color_str == 'AMBER':
            self.status = Color.AMBER
        elif color_str == 'GREEN':
            self.status = Color.GREEN

class Color(Enum):
    DEFAULT = 0
    RED = 1
    AMBER = 2
    GREEN = 3
