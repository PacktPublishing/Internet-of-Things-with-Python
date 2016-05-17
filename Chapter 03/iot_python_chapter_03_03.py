__author__ = 'Gaston C. Hillar'


import mraa
import time


class Led:
    def __init__(self, pin):
        self.gpio = mraa.Gpio(pin)
        self.gpio.dir(mraa.DIR_OUT)

    def turn_on(self):
        self.gpio.write(1)
        print("I've turned on the LED connected to GPIO Pin #{0}.".format(self.gpio.getPin()))


    def turn_off(self):
        self.gpio.write(0)
        print("I've turned off the LED connected to GPIO Pin #{0}.".format(self.gpio.getPin()))


if __name__ == "__main__":
    print ("Mraa library version: {0}".format(mraa.getVersion()))
    print ("Mraa detected platform name: {0}".format(mraa.getPlatformName()))

    # Configure GPIO pins #1 to 9 to be output pins
    leds = []
    for i in range(1, 10):
        led = Led(i)
        leds.append(led)

    # Count from 1 to 9
    for i in range(1, 10):
        print("==== Turning on {0} LEDs ====".format(i))
        for j in range(0, i):
            leds[j].turn_on()
        for k in range(i, 9):
            leds[k].turn_off()
        time.sleep(10)
