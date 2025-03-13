#import numpy as np
#from scipy.ndimage import label, sum_labels, center_of_mass
#from scipy.ndimage import gaussian_filter, uniform_filter
import datetime
import os
#import matplotlib.image as mpimg
#import matplotlib.pyplot as plt
#import gc
import sys
import math
#import psutil

#HODI = "/home/r2/"
#HODI = os.getcwd()+"/"
HODI = "/home/madiza/"
CAMNO = "0"
print (sys.argv)
try:    epo = sys.argv[1]
except: 
    LD = os.listdir(HODI+"RES"+CAMNO)
    #smassv = sorted(LD)
    LDN = [int(i) for i in LD]
    epo = str(sorted(LDN)[-1])
    #print(smassv)
    #print(LDN)
if 2>1:
  
  try:
  #if 2>1:
    with open(HODI+"RES"+"0"+"/"+epo+"/RA.csv","r") as fo:
      RLS0 = fo.readlines()
    #print(epo,'\t',len(RLS0))
    with open(HODI+"RES"+"1"+"/"+epo+"/RA.csv","r") as fo:
      RLS1 = fo.readlines()
    #print(epo,'\t',len(RLS1))
    D0 = {}
    D1 = {}
    LUXes0=str(epo)
    LUXes1=str(epo)
    for i in range(1,len(RLS0),1):
        sl = RLS0[i].replace("\n","").split("|")
        sln = sl[-1].split("-")[1]
        LUXes0 += " "+sl[0]
        try: D0[sln].append([int(sl[1]),int(sl[2]),float(sl[0]),float(sl[3]),float(sl[4])])
        except:D0[sln] = [[int(sl[1]),int(sl[2]),float(sl[0]),float(sl[3]),float(sl[4])]]
    for i in range(1,len(RLS1),1):
        sl = RLS1[i].replace("\n","").split("|")
        sln = sl[-1].split("-")[1]
        LUXes1 += " "+sl[0]
        try: D1[sln].append([int(sl[1]),int(sl[2]),float(sl[0]),float(sl[3]),float(sl[4])])
        except:D1[sln] = [[int(sl[1]),int(sl[2]),float(sl[0]),float(sl[3]),float(sl[4])]]
    #print(D0)
    #print(D1)
    with open("LU.txt","w") as fo:
        fo.write(LUXes0+"\n")
        fo.write(LUXes1)
    N2cadr = 0
    with open(HODI+"/RA.csv","w") as fo:
      for fn in D0:
        if fn in D1:
            #print(fn)
            N2cadr+=1
            #print(" ",D0[fn])
            #print(" ",D1[fn])
            sd = [str(D0[fn][k]) for k in range(len(D0[fn]))]+["_"]+[str(D1[fn][k]) for k in range(len(D1[fn]))]
            sdd = fn
            for k in range(len(sd)): sdd+="|"+sd[k]
            fo.write(sdd+"\n")

    with open("NU.txt","w") as fo:
        fo.write( str(epo)+" "+str(len(RLS0))+" "+str(len(RLS1)) +" "+str(N2cadr))

  except Exception as e: print(e)

