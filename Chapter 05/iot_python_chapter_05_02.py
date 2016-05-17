__author__ = 'Gaston C. Hillar'


from datetime import date
import mraa
import tornado.escape
import tornado.ioloop
import tornado.web
import logging

# Pin ~6 to connect the red LED
# Pin ~5 to connect the green LED
# Pin ~3 to connect the blue LED.


class AnalogLed:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        self.pwm = mraa.Pwm(pin)
        self.pwm.period_us(700)
        self.pwm.enable(True)
        self.brightness_value = 0
        self.set_brightness(0)

    def set_brightness(self, value):
        brightness_value = value
        if brightness_value > 255:
            brightness_value = 255
        elif brightness_value < 0:
            brightness_value = 0
        led_value = brightness_value / 255.0
        self.pwm.write(led_value)
        self.brightness_value = brightness_value
        print("{0} LED connected to PWM Pin #{1} set to brightness {2}.".format(self.name, self.pin, brightness_value))


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


class BoardInteraction:
    # The Red LED is connected to pin ~6
    red_led = AnalogLed(6, 'Red')
    # The Green LED is connected to Pin ~5
    green_led = AnalogLed(5, 'Green')
    # The Blue LED is connected to Pin ~3
    blue_led = AnalogLed(3, 'Blue')
    # The push button to reset colors
    reset_push_button = PushButton(1)
    # The push button to set colors to their maximum brightness
    max_brightness_push_button = PushButton(0)

    @classmethod
    def set_min_brightness(cls):
        cls.red_led.set_brightness(0)
        cls.green_led.set_brightness(0)
        cls.blue_led.set_brightness(0)

    @classmethod
    def set_max_brightness(cls):
        cls.red_led.set_brightness(255)
        cls.green_led.set_brightness(255)
        cls.blue_led.set_brightness(255)

    @classmethod
    def check_push_buttons_callback(cls):
        # Check whether the reset push button is pressed
        if cls.reset_push_button.is_pressed:
            print("You are pressing the reset pushbutton.")
            cls.set_min_brightness()

        # Check whether the maximum brightness push button is pressed
        if cls.max_brightness_push_button.is_pressed:
            print("You are pressing the maximum brightness pushbutton.")
            cls.set_max_brightness()


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': '1.0',
                    'last_build': date.today().isoformat()}
        self.write(response)


class PutRedBrightnessHandler(tornado.web.RequestHandler):
    def put(self, value):
        int_value = int(value)
        BoardInteraction.red_led.set_brightness(int_value)
        response = {'red': BoardInteraction.red_led.brightness_value}
        self.write(response)


class PutGreenBrightnessHandler(tornado.web.RequestHandler):
    def put(self, value):
        int_value = int(value)
        BoardInteraction.green_led.set_brightness(int_value)
        response = {'green': BoardInteraction.green_led.brightness_value}
        self.write(response)


class PutBlueBrightnessHandler(tornado.web.RequestHandler):
    def put(self, value):
        int_value = int(value)
        BoardInteraction.blue_led.set_brightness(int_value)
        response = {'blue': BoardInteraction.blue_led.brightness_value}
        self.write(response)


class PutMinBrightnessHandler(tornado.web.RequestHandler):
    def put(self):
        BoardInteraction.set_min_brightness()
        response = dict(
            red=BoardInteraction.red_led.brightness_value,
            green=BoardInteraction.green_led.brightness_value,
            blue=BoardInteraction.blue_led.brightness_value)
        self.write(response)


class PutMaxBrightnessHandler(tornado.web.RequestHandler):
    def put(self):
        BoardInteraction.set_max_brightness()
        response = dict(
            red=BoardInteraction.red_led.brightness_value,
            green=BoardInteraction.green_led.brightness_value,
            blue=BoardInteraction.blue_led.brightness_value)
        self.write(response)

class PutRGBBrightnessHandler(tornado.web.RequestHandler):
    def put(self, red, green, blue):
        int_red = int(red)
        int_green = int(green)
        int_blue = int(blue)
        BoardInteraction.red_led.set_brightness(int_red)
        BoardInteraction.green_led.set_brightness(int_green)
        BoardInteraction.blue_led.set_brightness(int_blue)
        response = dict(
            red=BoardInteraction.red_led.brightness_value,
            green=BoardInteraction.green_led.brightness_value,
            blue=BoardInteraction.blue_led.brightness_value)
        self.write(response)


class GetRedBrightnessHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'red': BoardInteraction.red_led.brightness_value}
        self.write(response)


class GetGreenBrightnessHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'green': BoardInteraction.green_led.brightness_value}
        self.write(response)


class GetBlueBrightnessHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'blue': BoardInteraction.blue_led.brightness_value}
        self.write(response)


application = tornado.web.Application([
    (r"/putredbrightness/([0-9]+)", PutRedBrightnessHandler),
    (r"/putgreenbrightness/([0-9]+)", PutGreenBrightnessHandler),
    (r"/putbluebrightness/([0-9]+)", PutBlueBrightnessHandler),
    (r"/putrgbbrightness/r([0-9]+)g([0-9]+)b([0-9]+)",
     PutRGBBrightnessHandler),
    (r"/putminbrightness", PutMinBrightnessHandler),
    (r"/putmaxbrightness", PutMaxBrightnessHandler),
    (r"/getredbrightness", GetRedBrightnessHandler),
    (r"/getgreenbrightness", GetGreenBrightnessHandler),
    (r"/getbluebrightness", GetBlueBrightnessHandler),
    (r"/version", VersionHandler)])


if __name__ == "__main__":
    print("Listening at port 8888")
    application.listen(8888)
    ioloop = tornado.ioloop.IOLoop.instance()
    periodic_callback = tornado.ioloop.PeriodicCallback(BoardInteraction.check_push_buttons_callback, 500, ioloop)
    periodic_callback.start()
    ioloop.start()
