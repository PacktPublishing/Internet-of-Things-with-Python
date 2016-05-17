__author__ = 'Gaston C. Hillar'


import pyupm_th02 as upmTh02
import pyupm_i2clcd as upmLcd
import pyupm_servo as upmServo
import time
from pubnub import Pubnub


class TemperatureServo:
    def __init__(self, pin):
        self.servo = upmServo.ES08A(pin)
        self.servo.setAngle(0)

    def print_temperature(self, temperature_fahrenheit):
        angle = temperature_fahrenheit
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        self.servo.setAngle(angle)


class Oled:
    # The I2C address for the OLED display
    oled_i2c_address = 0x3C

    def __init__(self, bus):
        self.oled = upmLcd.SSD1327(
            bus,
            self.__class__.oled_i2c_address)
        self.oled.clear()

    def print_line(self, row, message):
        self.oled.setCursor(row, 0)
        self.oled.setGrayLevel(12)
        self.oled.write(message)


class TemperatureAndHumidityOled(Oled):
    def print_temperature(self, temperature_fahrenheit, temperature_celsius):
        self.print_line(0, "Temperature")
        self.print_line(2, "Fahrenheit")
        self.print_line(3, "{:5.2f}".format(temperature_fahrenheit))
        self.print_line(5, "Celsius")
        self.print_line(6, "{:5.2f}".format(temperature_celsius))

    def print_humidity(self, humidity):
        self.print_line(8, "Humidity")
        self.print_line(9, "Level")
        self.print_line(10, "{0}%".format(humidity))


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


class MessageChannel:
    command_key = "command"
    successfully_processed_command_key = "successfully_processed_command"

    def __init__(self, channel, temperature_servo, oled):
        self.temperature_servo = temperature_servo
        self.oled = oled
        self.channel = channel
        # Do not forget to replace the string with your publish key
        publish_key = "pub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        # Subscribe key is the one that usually starts with the "sub-c" prefix
        # Do not forget to replace the string with your subscribe key
        subscribe_key = "sub-c-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        self.pubnub = Pubnub(publish_key=publish_key, subscribe_key=subscribe_key)
        self.pubnub.subscribe(channels=self.channel,
                              callback=self.callback,
                              error=self.callback,
                              connect=self.connect,
                              reconnect=self.reconnect,
                              disconnect=self.disconnect)

    def callback_response_message(self, message, channel):
        print("I've received the following response from PubNub cloud: {0}".format(message))

    def error_response_message(self, message):
        print("There was an error when working with the PubNub cloud: {0}".format(message))

    def publish_response_message(self, message):
        response_message = {
            self.__class__.successfully_processed_command_key:
                message[self.__class__.command_key]}
        self.pubnub.publish(
            channel=self.channel,
            message=response_message,
            callback=self.callback_response_message,
            error=self.error_response_message)

    def callback(self, message, channel):
        if channel == self.channel:
            print("I've received the following message: {0}".format(message))
            if self.__class__.command_key in message:
                if message[self.__class__.command_key] == "print_temperature_fahrenheit":
                    self.temperature_servo.print_temperature(message["temperature_fahrenheit"])
                    self.publish_response_message(message)
                elif message[self.__class__.command_key] == "print_information_message":
                    self.oled.print_line(11, message["text"])
                    self.publish_response_message(message)

    def error(self, message):
        print("Error: " + str(message))

    def connect(self, message):
        print("Connected to the {0} channel".
              format(self.channel))
        print(self.pubnub.publish(
            channel=self.channel,
            message="Listening to messages in the Intel Galileo Gen 2 board"))

    def reconnect(self, message):
        print("Reconnected to the {0} channel".
              format(self.channel))

    def disconnect(self, message):
        print("Disconnected from the {0} channel")


if __name__ == "__main__":
    temperature_and_humidity_sensor = \
        TemperatureAndHumiditySensor(0)
    oled = TemperatureAndHumidityOled(0)
    temperature_servo = TemperatureServo(3)
    message_channel = MessageChannel("temperature", temperature_servo, oled)
    while True:
        temperature_and_humidity_sensor.\
            measure_temperature_and_humidity()
        oled.print_temperature(
            temperature_and_humidity_sensor.temperature_fahrenheit,
            temperature_and_humidity_sensor.temperature_celsius)
        oled.print_humidity(
            temperature_and_humidity_sensor.humidity)
        print("Ambient temperature in degrees Celsius: {0}".
              format(temperature_and_humidity_sensor.temperature_celsius))
        print("Ambient temperature in degrees Fahrenheit: {0}".
              format(temperature_and_humidity_sensor.temperature_fahrenheit))
        print("Ambient humidity: {0}".
              format(temperature_and_humidity_sensor.humidity))
        # Sleep 10 seconds (10000 milliseconds)
        time.sleep(10)
