__author__ = 'Gaston C. Hillar'


import mraa
import time


if __name__ == "__main__":
    print ("Mraa library version: {0}".format(mraa.getVersion()))
    print ("Mraa detected platform name: {0}".format(mraa.getPlatformName()))

    # Configure GPIO pin #13 to be an output pin
    onboard_led = mraa.Gpio(13)
    onboard_led.dir(mraa.DIR_OUT)

    while True:
        # Turn on the onboard LED
        onboard_led.write(1)
        print("I've turned on the onboard LED.")
        # Sleep 3 seconds
        time.sleep(3)
        # Turn off the onboard LED
        onboard_led.write(0)
        print("I've turned off the onboard LED.")
        time.sleep(2)
