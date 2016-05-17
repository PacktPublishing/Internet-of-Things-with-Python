__author__ = 'Gaston C. Hillar'


import mraa
import time


if __name__ == "__main__":
    print ("Mraa library version: {0}".format(mraa.getVersion()))
    print ("Mraa detected platform name: {0}".format(mraa.getPlatformName()))

    # Configure GPIO pins #1 to 9 to be output pins
    output = []
    for i in range(1, 10):
        gpio = mraa.Gpio(i)
        gpio.dir(mraa.DIR_OUT)
        output.append(gpio)

    # Count from 1 to 9
    for i in range(1, 10):
        print("==== Turning on {0} LEDs ====".format(i))
        for j in range(0, i):
            output[j].write(1)
            print("I've turned on the LED connected to GPIO Pin #{0}.".format(j + 1))
        time.sleep(3)
