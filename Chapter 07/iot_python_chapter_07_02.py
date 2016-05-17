__author__ = 'Gaston C. Hillar'


import pyupm_adxl345 as upmAdxl345
import time


class Accelerometer:
    def __init__(self, bus):
        self.accelerometer = upmAdxl345.Adxl345(bus)
        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

    def measure_acceleration(self):
        # Update the acceleration values for the three axis
        self.accelerometer.update()
        # Retrieve the acceleration values for the three axis
        acceleration_array = \
            self.accelerometer.getAcceleration()
        self.x_acceleration = acceleration_array[0]
        self.y_acceleration = acceleration_array[1]
        self.z_acceleration = acceleration_array[2]


if __name__ == "__main__":
    accelerometer = Accelerometer(0)
    while True:
        accelerometer.measure_acceleration()
        print("Acceleration for x: {:5.2f}g".
              format(accelerometer.x_acceleration))
        print("Acceleration for y: {:5.2f}g".
              format(accelerometer.y_acceleration))
        print("Acceleration for z: {:5.2f}g".
              format(accelerometer.z_acceleration))
        # Sleep 0.5 seconds (500 milliseconds)
        time.sleep(0.5)
