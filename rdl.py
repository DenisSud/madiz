import serial
import time

ser = serial.Serial('/dev/ttyS0', 115200)

dr = "/home/madiza/"

with open(dr + "NU.txt", "r") as f:
	for i in f:
		ser.write(i.encode('ascii'))
ser.write("\n".encode('ascii'))
time.sleep(1)

with open(dr + "LU.txt", "r") as f:
	for i in f:
		"""cnt = 0
		ss = ""
		for j in i.split(" "):
			cnt += 1
			ss = ""
			ss += j
			if cnt == 10:
				cnt = 0
				ser.write(ss.encode('ascii'))
				ser.write("\n".encode('ascii'))
				ss = ""
			else:
				ss += " "
		"""
		ser.write(i.encode('ascii'))		
ser.write("\n".encode('ascii'))
time.sleep(1)

with open(dr + "RA.csv", "r") as f:
	for i in f:
		ser.write(i.encode('ascii'))
ser.write("\n".encode('ascii'))
time.sleep(1)
ser.close()
