__author__ = 'Gaston C. Hillar'


import mraa
import time


class VoltageInput:
    def __init__(self, analog_pin):
        self.analog_pin = analog_pin
        self.aio = mraa.Aio(analog_pin)
        # Configure ADC resolution to 12 bits (0 to 4095)
        self.aio.setBit(12)

    @property
    def voltage(self):
        raw_value = self.aio.read()
        return raw_value / 4095.0 * 5.0


if __name__ == "__main__":
    v0 = VoltageInput(0)
    while True:
        print("Voltage at pin A0: {0}".format(v0.voltage))
        # Sleep 2 seconds
        time.sleep(2)
