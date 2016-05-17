__author__ = 'Gaston C. Hillar'


import mraa
import time


class Adxl345:
    # Read buffer length
    READ_BUFFER_LENGTH = 6
    # I2C address for the ADXL345 accelerometer
    ADXL345_I2C_ADDR = 0x53
    ADXL345_ID = 0x00
    # Control registers
    ADXL345_OFSX = 0x1E
    ADXL345_OFSY = 0x1F
    ADXL345_OFSZ = 0x20
    ADXL345_TAP_THRESH = 0x1D
    ADXL345_TAP_DUR = 0x21
    ADXL345_TAP_LATENCY = 0x22
    ADXL345_ACT_THRESH = 0x24
    ADXL345_INACT_THRESH = 0x25
    ADXL345_INACT_TIME = 0x26
    ADXL345_INACT_ACT_CTL = 0x27
    ADXL345_FALL_THRESH = 0x28
    ADXL345_FALL_TIME = 0x29
    ADXL345_TAP_AXES = 0x2A
    ADXL345_ACT_TAP_STATUS = 0x2B
    # Interrupt registers
    ADXL345_INT_ENABLE = 0x2E
    ADXL345_INT_MAP = 0x2F
    ADXL345_INT_SOURCE = 0x30
    # Data registers (read only)
    ADXL345_XOUT_L = 0x32
    ADXL345_XOUT_H = 0x33
    ADXL345_YOUT_L = 0x34
    ADXL345_YOUT_H = 0x35
    ADXL345_ZOUT_L = 0x36
    ADXL345_ZOUT_H = 0x37
    DATA_REG_SIZE = 6
    # Data and power management
    ADXL345_BW_RATE = 0x2C
    ADXL345_POWER_CTL = 0x2D
    ADXL345_DATA_FORMAT = 0x31
    ADXL345_FIFO_CTL = 0x38
    ADXL345_FIFO_STATUS = 0x39
    # Useful values
    ADXL345_POWER_ON = 0x08
    ADXL345_AUTO_SLP = 0x30
    ADXL345_STANDBY = 0x00
    # Scales and resolution
    ADXL345_FULL_RES = 0x08
    ADXL345_10BIT = 0x00
    ADXL345_2G = 0x00
    ADXL345_4G = 0x01
    ADXL345_8G = 0x02
    ADXL345_16G = 0x03

    def __init__(self, bus):
        # Init bus and reset chip
        self.i2c = mraa.I2c(bus)
        # Set the slave to talk to
        if self.i2c.address(self.__class__.ADXL345_I2C_ADDR) != mraa.SUCCESS:
            raise Exception("i2c.address() failed")
        message = bytearray(
            [self.__class__.ADXL345_POWER_CTL,
             self.__class__.ADXL345_POWER_ON])
        if self.i2c.write(message) != mraa.SUCCESS:
            raise Exception("i2c.write() control register failed")
        if self.i2c.address(self.__class__.ADXL345_I2C_ADDR) != mraa.SUCCESS:
            raise Exception("i2c.address() failed")
        message = bytearray(
            [self.__class__.ADXL345_DATA_FORMAT,
             self.__class__.ADXL345_16G | self.__class__.ADXL345_FULL_RES])
        if self.i2c.write(message) != mraa.SUCCESS:
            raise Exception("i2c.write() mode register failed")
        # 2.5V sensitivity is 256 LSB/g = 0.00390625 g/bit
        # 3.3V x and y sensitivity is 265 LSB/g = 0.003773584 g/bit, z is the same
        self.x_offset = 0.003773584
        self.y_offset = 0.003773584
        self.z_offset = 0.00390625
        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0
        self.update()

    def update(self):
        # Set the slave to talk to
        self.i2c.address(self.__class__.ADXL345_I2C_ADDR)
        self.i2c.writeByte(self.__class__.ADXL345_XOUT_L)
        self.i2c.address(self.__class__.ADXL345_I2C_ADDR)
        xyz_raw_acceleration = self.i2c.read(self.__class__.DATA_REG_SIZE)
        x_raw_acceleration = (xyz_raw_acceleration[1] << 8) | xyz_raw_acceleration[0]
        y_raw_acceleration = (xyz_raw_acceleration[3] << 8) | xyz_raw_acceleration[2]
        z_raw_acceleration = (xyz_raw_acceleration[5] << 8) | xyz_raw_acceleration[4]
        self.x_acceleration = x_raw_acceleration * self.x_offset
        self.y_acceleration = y_raw_acceleration * self.y_offset
        self.z_acceleration = z_raw_acceleration * self.z_offset


class Accelerometer:
    def __init__(self, bus):
        self.accelerometer = Adxl345(bus)
        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

    def measure_acceleration(self):
        # Update the acceleration values for the three axis
        self.accelerometer.update()
        self.x_acceleration = self.accelerometer.x_acceleration
        self.y_acceleration = self.accelerometer.y_acceleration
        self.z_acceleration = self.accelerometer.z_acceleration


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
