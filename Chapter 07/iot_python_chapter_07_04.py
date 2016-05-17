__author__ = 'Gaston C. Hillar'


import pyupm_grove as upmGrove
import time


class TemperatureSensor:
    def __init__(self, analog_pin):
        self.temperature_sensor = upmGrove.GroveTemp(analog_pin)
        self.temperature_celsius = 0.0
        self.temperature_fahrenheit = 0.0

    def measure_temperature(self):
        # Retrieve the temperature expressed in Celsius degrees
        temperature_celsius = self.temperature_sensor.value()
        self.temperature_celsius = temperature_celsius
        self.temperature_fahrenheit = \
            (temperature_celsius * 9.0 / 5.0) + 32.0


if __name__ == "__main__":
    # The temperature sensor is connected to analog pin A0
    temperature_sensor = TemperatureSensor(0)

    while True:
        temperature_sensor.measure_temperature()
        print("Ambient temperature in degrees Celsius: {0}".
              format(temperature_sensor.temperature_celsius))
        print("Ambient temperature in degrees Fahrenheit: {0}".
              format(temperature_sensor.temperature_fahrenheit))
        # Sleep 10 seconds (10000 milliseconds)
        time.sleep(10)
