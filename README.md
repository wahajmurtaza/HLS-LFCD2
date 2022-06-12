# HLS-LFCD2 

This repo is for interfacing HLS-LFCD2 with python3 


##  ANGLE DIRECTIONS
		
LIDAR
		
		270
	180		0
		90


# SETUP

### Dependencies
* python3
* pyserial

### Pins Connection
* RED       5V
* BROWN     TX
* ORANGE    PWM     (connect with pwm) # ground internally
* BLACK     GND
* GREEN     RX
* BLUE      BOT     (not used)

Other Connector
* BLACK     PWM     (connect with pwm)
* RED       5V

### CODE
```python
from hls_lfcd2 import Lidar
from time import sleep

lidar = Lidar("COM6", angle_offset=0)
lidar.start()

# required to obtain valid data of 360 degress
sleep(2)

print(f'rpm = {lidar.get_rpm()}')
print(f'distance = {lidar.get_distance()}')
print(f'intensity = {lidar.get_intensity()}')

# stopped lidar can be started again
lidar.stop()

# once termindated, it can not be started
lidar.terminate()

```

# CONTACT
In case of any query you can contact at

* https://github.com/wahajmurtaza
* wahajmurtaza@gmail.com
