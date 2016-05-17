__author__ = 'Gaston C. Hillar'


import mraa
from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web


class Led:
    def __init__(self, pin, position):
        self.position = position
        self.gpio = mraa.Gpio(pin)
        self.gpio.dir(mraa.DIR_OUT)

    def turn_on(self):
        self.gpio.write(1)
        print("I've turned on the LED connected to GPIO Pin #{0}, in position {1}.".format(self.gpio.getPin(), self.position))


    def turn_off(self):
        self.gpio.write(0)
        print("I've turned off the LED connected to GPIO Pin #{0}, in position {1}.".format(self.gpio.getPin(), self.position))


class NumberInLeds:
    def __init__(self):
        self.leds = []
        for i in range(9, 0, -1):
            led = Led(i, 10 - i)
            self.leds.append(led)

    def print_number(self, number):
        print("==== Turning on {0} LEDs ====".format(number))
        for j in range(0, number):
            self.leds[j].turn_on()
        for k in range(number, 9):
            self.leds[k].turn_off()


class BoardInteraction:
    number_in_leds = NumberInLeds()
    current_number = 0


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': '1.0',
                    'last_build': date.today().isoformat()}
        self.write(response)


class PutNumberInLedsHandler(tornado.web.RequestHandler):
    def put(self, number):
        int_number = int(number)
        BoardInteraction.number_in_leds.print_number(int_number)
        BoardInteraction.current_number = int_number
        response = {'number': int_number}
        self.write(response)


class GetCurrentNumberHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'number': BoardInteraction.current_number}
        self.write(response)


application = tornado.web.Application([
    (r"/putnumberinleds/([0-9])", PutNumberInLedsHandler),
    (r"/getcurrentnumber", GetCurrentNumberHandler),
    (r"/version", VersionHandler)])


if __name__ == "__main__":
    print("Listening at port 8888")
    BoardInteraction.number_in_leds.print_number(0)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
