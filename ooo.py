import time
import os
from picamera2.controls import Controls
from picamera2 import Picamera2, Preview

from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.ndimage import label, sum_labels, center_of_mass
from scipy.ndimage import gaussian_filter, uniform_filter
import datetime
import json

import sys
nay00 =  datetime.datetime.now()
numca = 0
try: numca = int(sys.argv[1])
except: pass
try: Ndir = sys.argv[2]
except: Ndir = "0"

print ("cam #",numca,datetime.datetime.now())
'''exit()'''
picam0 = Picamera2(numca)
picam0.start_preview(Preview.NULL)

preview_config = picam0.create_preview_configuration()
#capture_config = picam0.create_still_configuration()
capture_config = picam0.create_still_configuration(main={"size": (2028, 1520)})
picam0.configure(preview_config)
picam0.options["compress_level"] = 2
picam0.start()

#time.sleep(2)

ctrls0 = Controls(picam0)
ctrls0.AnalogueGain = 1.0
ctrls0.ExposureTime = 1000000 #1000000

picam0.set_controls(ctrls0)

time.sleep(1)

request0 = picam0.capture_request()


datatt = str(datetime.datetime.now())#.split(" ")[0]
#if datatt not in os.listdir(str(numca)):
#     os.mkdir(str(numca) + "/" + datatt)

HODI = "/home/madiza/"
#HODI = ""
CAMNO = str(numca)
MOBdir = HODI+"MOB"+CAMNO
try: os.makedirs(MOBdir)
except: pass
#LD = os.listdir(MOBdir)
#Ndir = str(len(LD))
#try: os.makedirs(MOBdir+"/"+Ndir)
#except: pass

fna0 = MOBdir+"/"+Ndir+"/"+CAMNO+"-"+datatt.split(" ")[0].replace("-","")[2:]+"_"+datatt.split(" ")[1].replace(":","")[:6]

#sfiles = "/home/madiza/madiz/OBE/"+str(numca)+"/" + datatt + "/"
#data = io.BytesIO()
print("camera #",numca)
nay0 =  datetime.datetime.now()
imag0 = picam0.switch_mode_and_capture_array(capture_config, "main")
time_cam0 = str(datetime.datetime.now())

#fna0=sfiles + "i"+str(numca)+"_"+str(datetime.datetime.now()).replace(" ","_")[:18] #+".npy"
print("1111111111111111111",fna0, datetime.datetime.now() - nay0)

#print(data.getbuffer().nbytes)
#print(len(data.getbuffer()))
#array = picam2.capture_array(capture_config)
print(len(imag0))


metadata0 = request0.get_metadata()
request0.release()  # requests must always be returned to libcamera



print(metadata0["SensorTemperature"])
sensor_temp0 = metadata0["SensorTemperature"]


#np.save(fna0, imag0)
picam0.close()
im = Image.fromarray(imag0)
im.save(fna0+".png")
print("222222222222222",fna0, datetime.datetime.now() - nay00)
#np.save(fna0,imag0)
#print("333333333333333",fna0, datetime.datetime.now() - nay00)





#print(fna0," file saved ")
#print(datetime.datetime.now())
#exit()
#cam0
#if numca == 0:
#    time.sleep(15)

#g1 = np.dot(imag0[...,:3], [0.2989, 0.5870, 0.1140])
#g2 = np.dot(imag00[...,:3], [0.2989, 0.5870, 0.1140])

#gm = g1#np.subtract(g2,g1)   #  вычитаются битые пиксели
#del imag0
#del imag00
#del g2
#del g1

#gm = abs(gm)    # вычитаемый кадр - тоже инфа.. зачем ее выбрасывать?
#gm = uniform_filter(gm, size=4) #сглаживаем по 4х4
#bk = np.sqrt(uniform_filter(gm**2, size=200)) #root mean squares over square 200*200
#gn = gm.copy()
#gn[gn < bk * 5] = 0  # все < 5 sigma считаем шумом и обнуляем. получаются изолированние треки 
#del bk

#kernel = np.ones((3, 3))
#l, n = label(gn, structure=kernel) #каждому треку приписывается номер (начитается с первого)))
#print(len(l), n)
#ind = [i for i in range(1,n+1,1)]
#su = sum_labels(gn, labels=l, index=ind)  # вектор яркостей для каждого пронумерованного трека
#cm = center_of_mass(gn, labels=l, index=ind) # вектор центров тяжестей для каждого пронумерованного трека
#сортируем по убыванию яркости
#ar = [[ind[i],su[i],cm[i]] for i in range(len(ind))] #3 столбца
#del su
#del cm
#ra=sorted(ar,key=lambda l:l[1], reverse=True)  # сортирует по 2-му (яркости)
#del ar
#count_cam0 = n


#with open(sfiles + datatt + "datas.txt", "a") as f:
#     f.write(str(numca) + " " + str(time_cam0) + " " + str(count_cam0) + " " + str(sensor_temp0) + "\n")

