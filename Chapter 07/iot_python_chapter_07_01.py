__author__ = 'Gaston C. Hillar'


import pyupm_adxl335 as upmAdxl335
import time


class Accelerometer:
    def __init__(self, pinX, pinY, pinZ):
        self.accelerometer = upmAdxl335.ADXL335(
            pinX, pinY, pinZ)
        self.x_acceleration_fp = upmAdxl335.new_floatPointer()
        self.y_acceleration_fp = upmAdxl335.new_floatPointer()
        self.z_acceleration_fp = upmAdxl335.new_floatPointer()
        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

    def calibrate(self):
        self.accelerometer.calibrate()

    def measure_acceleration(self):
        # Retrieve the acceleration values for the three axis
        self.accelerometer.acceleration(
            self.x_acceleration_fp,
            self.y_acceleration_fp,
            self.z_acceleration_fp)
        self.x_acceleration = upmAdxl335.floatPointer_value(
            self.x_acceleration_fp)
        self.y_acceleration = upmAdxl335.floatPointer_value(
            self.y_acceleration_fp)
        self.z_acceleration = upmAdxl335.floatPointer_value(
            self.z_acceleration_fp)


if __name__ == "__main__":
    # The accelerometer is connected to analog pins A0, A1 and A2
    # A0 -> x
    # A1 -> y
    # A2 -> z
    accelerometer = Accelerometer(0, 1, 2)
    # Calibrate the accelerometer
    accelerometer.calibrate()

    while True:
        accelerometer.measure_acceleration()
        print("Acceleration for x: {0}g".format(accelerometer.x_acceleration))
        print("Acceleration for y: {0}g".format(accelerometer.y_acceleration))
        print("Acceleration for z: {0}g".format(accelerometer.z_acceleration))
        # Sleep 0.5 seconds (500 milliseconds)
        time.sleep(0.5)
