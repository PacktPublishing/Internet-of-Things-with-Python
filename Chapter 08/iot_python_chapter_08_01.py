__author__ = 'Gaston C. Hillar'


import pyupm_th02 as upmTh02
import pyupm_i2clcd as upmLcd
import time


class Lcd:
    # The I2C address for the LCD display
    lcd_i2c_address = 0x3E
    # The I2C address for the RBG backlight
    rgb_i2c_address = 0x62

    def __init__(self, bus, red, green, blue):
        self.lcd = upmLcd.Jhd1313m1(
            bus,
            self.__class__.lcd_i2c_address,
            self.__class__.rgb_i2c_address)
        self.lcd.clear()
        self.set_background_color(red, green, blue)

    def set_background_color(self, red, green, blue):
        self.lcd.setColor(red, green, blue)

    def print_line_1(self, message):
        self.lcd.setCursor(0, 0)
        self.lcd.write(message)

    def print_line_2(self, message):
        self.lcd.setCursor(1, 0)
        self.lcd.write(message)


class TemperatureAndHumidityLcd(Lcd):
    def print_temperature(self, temperature_fahrenheit):
        self.print_line_1("Temp.    {:5.2f}F".format(temperature_fahrenheit))

    def print_humidity(self, humidity):
        self.print_line_2("Humidity   {0}%".format(humidity))


class TemperatureAndHumiditySensor:
    def __init__(self, bus):
        self.th02_sensor = upmTh02.TH02(bus)
        self.temperature_celsius = 0.0
        self.temperature_fahrenheit = 0.0
        self.humidity = 0.0

    def measure_temperature_and_humidity(self):
        # Retrieve the temperature expressed in Celsius degrees
        temperature_celsius = self.th02_sensor.getTemperature()
        self.temperature_celsius = temperature_celsius
        self.temperature_fahrenheit = \
            (temperature_celsius * 9.0 / 5.0) + 32.0
        # Retrieve the humidity
        self.humidity = self.th02_sensor.getHumidity()


if __name__ == "__main__":
    temperature_and_humidity_sensor = \
        TemperatureAndHumiditySensor(0)
    lcd = TemperatureAndHumidityLcd(0, 0, 0, 128)

    while True:
        temperature_and_humidity_sensor.\
            measure_temperature_and_humidity()
        lcd.print_temperature(
            temperature_and_humidity_sensor.temperature_fahrenheit)
        lcd.print_humidity(
            temperature_and_humidity_sensor.humidity)
        print("Ambient temperature in degrees Celsius: {0}".
              format(temperature_and_humidity_sensor.temperature_celsius))
        print("Ambient temperature in degrees Fahrenheit: {0}".
              format(temperature_and_humidity_sensor.temperature_fahrenheit))
        print("Ambient humidity: {0}".
              format(temperature_and_humidity_sensor.humidity))
        # Sleep 10 seconds (10000 milliseconds)
        time.sleep(10)
