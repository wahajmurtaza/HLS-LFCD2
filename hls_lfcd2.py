"""
This is code to interact lidar: HLS-LFCD2 with python3.
:author: Wahaj Murtaza
:github: https://github.com/wahajmurtaza
:email: wahajmurtaza@gmail.com
"""

import serial
from time import sleep
import threading

# LIDAR DATASHEET: https://emanual.robotis.com/assets/docs/LDS_Basic_Specification.pdf

# RED       5V
# BROWN     TX
# ORANGE    PWM     (connect with pwm) # ground internally
# BLACK     GND
# GREEN     RX
# BLUE      BOT     (not used)

# BLACK     PWM     (connect with pwm)
# RED       5V


class Lidar:
    distance = [0] * 360
    intensity = [0] * 360
    rpm = 0
    keep_loop = True

    def __init__(self, port, angle_offset=0):
        """
        Initiate Lidar object, aquire serial port, set parameters and start a lidar thread
        :param port: Serial Port at which lidar is connected
        :param angle_offset: Angle Offset (to adjust the front at zero) { 0 > angle_offset < 360 }
        """
        self.ser = serial.Serial(port=port, baudrate=230400)
        self.angle_offset = angle_offset
        self.thread = threading.Thread(target=self._start_loop)
        self.thread.start()

    def _read_serial(self):
        """
        read serial data (42 bytes)
        :return: serial data
        """
        data = self.ser.read(42)
        return data

    def _read_range(self, data):
        """
        read parameters from data
        :param data: serial data
        :return: None
        """
        bytes_data = list(data)

        degree = (bytes_data[1] - 0xA0) * 6
        self.rpm = (bytes_data[3] << 8) | bytes_data[2]

        if bytes_data[41] != bytes_data[40]  or bytes_data[40] == 0:
            print(f'invalid data: {degree}')
            return

        for i in range(6):
            distance = (bytes_data[2 + (i*4)+3] << 8) | (bytes_data[2 + (i*4)+2])
            intensity = (bytes_data[2 + (i*4)+1] << 8) | (bytes_data[2 + (i*4)+0])
            angle = degree + i
            angle_offsetted = angle + self.angle_offset if angle + self.angle_offset < 360 else angle + self.angle_offset - 360
            self.distance[angle_offsetted] = distance
            self.intensity[angle_offsetted] = intensity

    def start(self):
        """
        start the lidar
        :return: None
        """
        self.ser.write(b'b')

    def stop(self):
        """
        stop the lidar, can be started again
        :return: None
        """
        self.ser.write(b'e')

    def _start_loop(self):
        """
        Start the lidar loop (must be called in a separate thread)
        :return: None
        """
        while self.keep_loop:
            data = self._read_serial()
            if data[0] != 250:
                self.ser.write(b'e')
                self.ser.close()
                sleep(0.1)
                self.ser.open()
                self.ser.write(b'b')
                continue
            self._read_range(data)

    def terminate(self):
        """
        stop the leader, close serial port, and terminate thread
        :return: None
        """
        self.stop()
        self.keep_loop = False
        self.ser.close()
        self.thread.join()

    def get_distance(self):
        """
        get lidar distace
        :return: return distance array 1x360
        """
        return self.distance

    def get_intensity(self):
        """
        get lidar intensity
        :return: return intensity array 1x360
        """
        return self.intensity

    def get_rpm(self):
        """
        get lidar RPM
        :return: int
        """
        return self.rpm


if __name__ == '__main__':
    lidar = Lidar("COM6", angle_offset=0)

    lidar.start()

    sleep(2)
    print(f'rpm = {lidar.get_rpm()}')
    print(f'distance = {lidar.get_distance()}')
    print(f'intensity = {lidar.get_intensity()}')

    lidar.stop()

    lidar.terminate()
