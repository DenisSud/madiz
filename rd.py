import sys
import os
import json
import serial
import time

sal = sys.argv[1].split('-') 
a = int(sal[0])
b = int(sal[1])
nc = int(sal[2])
dr = "/home/madiza/RES" + str(int(nc)) + "/"
#ser = serial.Serial('/dev/ttyS0', 115200)

for i in os.listdir(dr):
	#try:
		if int(i) >= a and int(i) <= b:
				ser = serial.Serial('/dev/ttyS0', 115200)

				ndr = dr + i + "/"
				with open(ndr + "NU.txt", "r") as f:
					for i in f:
						ser.write(i.encode('ascii'))
						print(i)
				ser.write("\n".encode('ascii'))
				time.sleep(1)

				with open(ndr + "LU.txt", "r") as f:
					for i in f:
						print(i)
						ser.write(i.encode('ascii'))		
				ser.write("\n".encode('ascii'))
				time.sleep(1)

				with open(ndr + "RA.csv", "r") as f:
					for i in f:
						print(i)
						ser.write(i.encode('ascii'))
				ser.write("\n".encode('ascii'))
				time.sleep(1)
				ser.close()
									
	#except:
	#  	print("errordir1")
	
	
