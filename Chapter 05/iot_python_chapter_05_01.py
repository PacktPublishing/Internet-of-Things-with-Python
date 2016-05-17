__author__ = 'Gaston C. Hillar'


import mraa
import time
from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import logging


class PushButton:
    def __init__(self, pin, pull_up=True):
        self.pin = pin
        self.pull_up = pull_up
        self.gpio = mraa.Gpio(pin)
        self.gpio.dir(mraa.DIR_IN)

    @property
    def is_pressed(self):
        push_button_status = self.gpio.read()
        if self.pull_up:
            # Pull-up resistor connected
            return push_button_status == 0
        else:
            # Pull-down resistor connected
            return push_button_status == 1

    @property
    def is_released(self):
        return not self.is_pressed


if __name__ == "__main__":
    s1_push_button = PushButton(1)
    s2_push_button = PushButton(0)
    while True:
        # Check whether the S1 pushbutton is pressed
        if s1_push_button.is_pressed:
            print("You are pressing S1.")
        # Check whether the S2 pushbutton is pressed
        if s2_push_button.is_pressed:
            print("You are pressing S2.")
        # Sleep 500 milliseconds (0.5 seconds)
        time.sleep(0.5)
