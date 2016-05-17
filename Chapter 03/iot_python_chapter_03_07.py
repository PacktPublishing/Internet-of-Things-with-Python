__author__ = 'Gaston C. Hillar'


from wiringx86 import GPIOGalileoGen2 as GPIO
import time


class Board:
    gpio = GPIO(debug=False)


class Led:
    def __init__(self, pin, position):
        self.pin = pin
        self.position = position
        self.gpio = Board.gpio
        self.gpio.pinMode(pin, self.gpio.OUTPUT)

    def turn_on(self):
        self.gpio.digitalWrite(self.pin, self.gpio.HIGH)
        print("I've turned on the LED connected to GPIO Pin #{0}, in position {1}.".format(self.pin, self.position))

    def turn_off(self):
        self.gpio.digitalWrite(self.pin, self.gpio.LOW)
        print("I've turned off the LED connected to GPIO Pin #{0}, in position {1}.".format(self.pin, self.position))


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


if __name__ == "__main__":
    print ("Working with wiring-x86 on Intel Galileo Gen 2")

    number_in_leds = NumberInLeds()
    # Count from 0 to 9
    for i in range(0, 10):
        number_in_leds.print_number(i)
        time.sleep(3)
