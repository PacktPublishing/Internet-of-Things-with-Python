__author__ = 'Gaston C. Hillar'


import pyupm_th02 as upmTh02
import pyupm_i2clcd as upmLcd
import pyupm_servo as upmServo
import time
import paho.mqtt.client as mqtt
import json


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

    def __init__(self, bus, red, green, blue):
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
        self.oled.clear()
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


class MessageTopic:
    command_key = "command"
    successfully_processed_command_key = "successfully_processed_command"
    # Replace with your own topic name
    topic = "iot-python-gaston-hillar/temperature"
    active_instance = None

    def __init__(self, temperature_servo, oled):
        self.temperature_servo = temperature_servo
        self.oled = oled
        self.client = mqtt.Client()
        self.client.on_connect = MessageTopic.on_connect
        self.client.on_message = MessageTopic.on_message
        self.client.connect(host="iot.eclipse.org",
                            port=1883,
                            keepalive=60)
        MessageTopic.active_instance = self

    def loop(self):
        self.client.loop()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected to the {0} topic".
              format(MessageTopic.topic))
        subscribe_result = client.subscribe(MessageTopic.topic)
        publish_result_1 = client.publish(
            topic=MessageTopic.topic,
            payload="Listening to messages in the Intel Galileo Gen 2 board")

    @staticmethod
    def on_message(client, userdata, msg):
        if msg.topic == MessageTopic.topic:
            print("I've received the following message: {0}".format(str(msg.payload)))
            try:
                message_dictionary = json.loads(msg.payload)
                if MessageTopic.command_key in message_dictionary:
                    if message_dictionary[MessageTopic.command_key] == "print_temperature_fahrenheit":
                        MessageTopic.active_instance.temperature_servo.print_temperature(
                            message_dictionary["temperature_fahrenheit"])
                        MessageTopic.active_instance.publish_response_message(
                            message_dictionary)
                    elif message_dictionary[MessageTopic.command_key] == "print_information_message":
                        MessageTopic.active_instance.oled.print_line(
                            11, message_dictionary["text"])
                        MessageTopic.active_instance.publish_response_message(message_dictionary)
            except ValueError:
                # msg is not a dictionary
                # No JSON object could be decoded
                pass

    def publish_response_message(self, message):
        response_message = json.dumps({
            self.__class__.successfully_processed_command_key:
                message[self.__class__.command_key]})
        result = self.client.publish(topic=self.__class__.topic,
                                payload=response_message)
        return result


if __name__ == "__main__":
    temperature_and_humidity_sensor = \
        TemperatureAndHumiditySensor(0)
    oled = TemperatureAndHumidityOled(0)
    temperature_servo = TemperatureServo(3)
    message_topic = MessageTopic(temperature_servo, oled)
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
        # Sleep 10 seconds (10000 milliseconds) but process messages every 1 second
        for i in range(0, 10):
            message_topic.loop()
            time.sleep(1)
