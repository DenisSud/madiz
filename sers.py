import serial
import time

ser = serial.Serial('/dev/ttyS0', 115200)

while 1:
	data = "Hello, world!\n"
	ser.write(data.encode('ascii'))	
	time.sleep(1)
ser.close()
