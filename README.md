#Internet of Things with Python

This is the code repository for [Internet of Things with Python](https://www.packtpub.com/hardware-and-creative/internet-things-python?utm_source=GitHub&utm_medium=Repository&utm_campaign=9781785881381
), published by Packt. It contains all the supporting project files necessary to work through the book from start to finish.

##Instructions and Navigation

The code included with this book is meant for use as an aid in performing the exercises and should not be used as a replacement for the book itself.
Used out of context, the code may result in an unusable configuration and no warranty is given.

The code will look like the following:
```
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

```


##Related OpenStack Products:

* [Internet of Things with the Arduino Yún](https://www.packtpub.com/hardware-and-creative/internet-things-arduino-y%C3%BAn?utm_source=GitHub&utm_medium=Repository&utm_campaign=9781783288007)

