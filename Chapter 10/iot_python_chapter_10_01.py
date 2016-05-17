__author__ = 'Gaston C. Hillar'


import pyupm_th02 as upmTh02
import pyupm_i2clcd as upmLcd
import pyupm_servo as upmServo
import time
import json
import sys
import requests
import uuid


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


class IntelIotAnalytics:
    base_url = "https://dashboard.us.enableiot.com/v1/api"
    # You can retrieve the following information from the My Account page
    account_name = "Temperature and humidity"
    account_id = "22612154-0f71-4f64-a68e-e116771115d5"
    # You can retrieve the device token with the following command:
    # cat /usr/lib/node_modules/iotkit-agent/data/device.json
    device_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiJjOTNmMTJhMy05MWZlLTQ3MWYtODM4OS02OGM1NDYxNDIxMDUiLCJpc3MiOiJodHRwOi8vZW5hYmxlaW90LmNvbSIsInN1YiI6ImthbnNhcy10ZW1wZXJhdHVyZS1odW1pZGl0eS0wMSIsImV4cCI6IjIwMjYtMDQtMDZUMTk6MDA6MTkuNzA0WiJ9.PH5yQas2FiQvUSR9V2pa3n3kIYZvmSe_xXY7QkFjlXUVUcyy9Sk_eVF4AL6qpZlBC9vjtd0L-VMZiULC9YXxAVl9s5Cl8ZqpQs36E1ssv_1H9CBFXKiiPArplzaWXVzvIRBVVzwfQrGrMoD_l4DcHlH2zgn5UGxhZ3RMPUvqgeneG3P-hSbPScPQL1pW85VT2IHT3seWyW1c637I_MDpHbJJCbkytPVpJpwKBxrCiKlGhvsh5pl4eLUXYUPlQAzB9QzC_ohujG23b-ApfHZugYD7zJa-05u0lkt93EEnuCk39o5SmPmIiuBup-k_mLn_VMde5fUvbxDt_SMI0XY3_Q"
    device_id = "kansas-temperature-humidity-01"
    component_id_temperature_fahrenheit = "0f3b3aae-ce40-4fb4-a939-e7c705915f0c"
    component_id_temperature_celsius = "c37cb57d-002c-4a66-866e-ce66bc3b2340"
    component_id_humidity_level_percentage = "71aba984-c485-4ced-bf19-c0f32649bcee"

    def publish_observation(self,
                            temperature_fahrenheit,
                            temperature_celsius,
                            humidity_level):
        url = "{0}/data/{1}".\
            format(self.__class__.base_url, self.__class__.device_id)
        now = int(time.time()) * 1000
        body = {
            "on": now,
            "accountId": self.__class__.account_id,
            "data": []
        }
        temperature_celsius_data = {
            "componentId": self.__class__.component_id_temperature_celsius,
            "on": now,
            "value": str(temperature_celsius)
        }
        temperature_fahrenheit_data = {
            "componentId": self.__class__.component_id_temperature_fahrenheit,
            "on": now,
            "value": str(temperature_fahrenheit)
        }
        humidity_level_percentage_data = {
            "componentId": self.__class__.component_id_humidity_level_percentage,
            "on": now,
            "value": str(humidity_level)
        }
        body["data"].append(temperature_celsius_data)
        body["data"].append(temperature_fahrenheit_data)
        body["data"].append(humidity_level_percentage_data)
        data = json.dumps(body)
        headers = {
            'Authorization': 'Bearer ' + self.__class__.device_token,
            'content-type': 'application/json'
        }
        response = requests.post(url, data=data, headers=headers, proxies={}, verify=True)
        if response.status_code != 201:
            print "The request failed. Status code: {0}. Response text: {1}.".\
                format(response.status_code, response.text)


if __name__ == "__main__":
    temperature_and_humidity_sensor = \
        TemperatureAndHumiditySensor(0)
    oled = TemperatureAndHumidityOled(0)
    intel_iot_analytics = IntelIotAnalytics()
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
        intel_iot_analytics.publish_observation(
            temperature_and_humidity_sensor.temperature_fahrenheit,
            temperature_and_humidity_sensor.temperature_celsius,
            temperature_and_humidity_sensor.humidity
        )
        # Sleep 5 seconds (5000 milliseconds)
        time.sleep(5)
