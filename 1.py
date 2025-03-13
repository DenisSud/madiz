import numpy as np
from scipy.ndimage import label, sum_labels, center_of_mass
from scipy.ndimage import gaussian_filter, uniform_filter
import datetime
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import gc
import sys
import math
#import psutil

import serial

ser = serial.Serial('/dev/ttyS0', 115200)
ser.write("tettttt".encode('ascii'))
#ser.close()



def morph(W):

            print("morph:")
            #print(W)

            rms = 0#np.sqrt(np.mean(W**2))
            print(" morph rms",rms)
            w = []#W.flatten()
            x = []#[0]*len(w)
            y = []#[0]*len(w)
            #jj = 0
            A=[]
            p3 = []
            mx = 0
            my = 0
            mw = 0
            swx = 0
            cmx = 0
            cmy = 0
            yav = 0 
            for jy in range(W.shape[0]):
             for jx in range(W.shape[1]):
               if W[jy][jx]>rms: #  0.0099:
                    x.append(jx)
                    y.append(jy)
                    w.append((W[jy][jx])**2)
                    A.append([jx,1])
                    p3.append([jx,jy])
                    if mw<W[jy][jx]:
                        mw = W[jy][jx]
                        mx = jx
                        my = jy
                    swx += W[jy][jx]
                    cmx += W[jy][jx] * jx
                    cmy += W[jy][jx] * jy
                    yav += jy
            cmx = mx
            cmy = my
            yav = yav/len(y)
            A = np.asarray(A)
            print("len w",len(w)," of ",W.shape[0]*W.shape[1])
            WW = np.diag(w)
            AW = np.dot(A.T,WW)
            AWA= np.dot(AW,A)
            AAm = np.linalg.pinv(AWA)
            RR = np.dot(AAm,A.T)
            RRW = np.dot(RR,WW)
            Rksi = np.dot(RRW,y)
            xa = 0
            ya = 0
            swx = 0

            for j in range(len(x)):
                #swx+= w[j]
                xa += x[j]
                ya += y[j]
                swx+=1
            xa = xa/swx
            ya = ya/swx
       
            xiyi = 0
            xi2 = 0
            yi2 = 0
            for j in range(len(x)):
                xiyi += (x[j]-xa)*(y[j]-ya)#*w[j]
                xi2 += (x[j]-xa)**2#*w[j]
                yi2 += (y[j]-ya)**2#*w[j]
            if xi2 !=0: a = xiyi/xi2
            else: a = 0
            b = ya -a*xa
            if xi2 !=0 and yi2 !=0: r2 = xiyi*2/xi2/yi2
            else: r2 = 0

            print("a=",a,b,xa,ya,r2)
            #ling = linregress(x,y)
            #print(ling)
            #a = ling.slope
            #b = ling.intercept
            

            a = Rksi[0]
            if a==0: a = 0.00001
            b = Rksi[1]
            bp = cmy+cmx/a
            #bp = ya+xa/a
            print(cmy,cmx,bp)
            
            p1 = np.array([5,a*5.+b])
            p1p= np.array([5,-5./a+bp])
            p2 = np.array([25,a*25.+b])

            p2p= np.array([25,-25./a+bp])
            p3 = np.array(p3)
            
            di=np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
            #print("np.linalg.norm(p2 -p1 )",np.linalg.norm(p2-p1))
            d = di * w 
            #print("p3",p3)
            #print(p1p)
            #print(p2p)
            #print(p3-p1p)
            #print(p2p-p1p)
            #print(np.cross(p2p-p1p,p3-p1p))
            di=np.cross(p2p-p1p,p3-p1p)/np.linalg.norm(p2p-p1p)
            #print("np.linalg.norm(p2p-p1p)",np.linalg.norm(p2p-p1p))
            dp = di * w 

            D = np.zeros( W.shape )
            DP = np.zeros( W.shape )
            for i in range (len(x)):
                D[y[i],x[i]]=d[i]
                DP[y[i],x[i]]=dp[i]
            print(" morph rms",rms)
            #print("d",d)
            #print("d",dp)
            #print("D ",(D * D).sum())
            #print("DP",(DP * DP).sum())
            #print("sqra",math.sqrt((DP * DP).sum() / (D * D).sum()))
            #print("  ra",(abs(DP)).sum() / (abs(D)).sum())
            ra = (abs(DP)).sum() / (abs(D)).sum()
            if ra<1 and ra !=0 : 
                    ra = 1./ra
                    b = cmy + cmx/a
                    a = -1./a
            SStot = 0
            SSres = 0
            for i in range(len(x)):
                SStot += (a*x[i]+b-yav)**2
                SSres += (a*x[i]+b-y[i])**2
            if SStot != 0: R2 = 1.- SSres/SStot
            else: R2 = 0
            print("morph:  a,b,ra,R2",a,b,ra,R2)
            return a,b,D,DP, ra, R2,cmy,cmx


nay00 = datetime.datetime.now()
#HODI = os.getcwd()+"/"
#HODI = "/home/r2/"
HODI = "/home/madiza/"

try:
    with open(HODI+"m.cfg","r") as fo:
        lcfg = fo.readlines()
        print (lcfg)
        ot = float(lcfg[0].replace("\n",""))
except: 
    ot = 0.1
    with open(HODI+"m.cfg","w") as fo:
        fo.write(str(ot))

print (sys.argv)
try:    CAMNO = sys.argv[1]
except: CAMNO = "0"

maxLX = 0
RA = []
PODC = {}

MOBdir = HODI+"MOB"+CAMNO
MD = os.listdir(MOBdir)
print(MD)
#inpa = input()

try:    Ndir = int(sys.argv[2])
except: Ndir = len(MD)-1
ser.write(str(Ndir).encode('ascii'))
ser.close()
if not str(Ndir) in MD:    # > len(MD)-1: 
    exit()
Ndir = str(Ndir)
print(Ndir)
LD = os.listdir(MOBdir+"/"+Ndir)
LD.sort()
print (LD)

for ild in range(0,len(LD),1):

  I = LD[ild]

#for I in range(1,20,1):
  
  try:
  #if 2>1:
    #imag1 = mpimg.imread("FON01sv/"+str(I)+".png")
    if "png" in I: imag1 = mpimg.imread(MOBdir+"/"+Ndir+"/"+I)
    else:          imag1 = np.load(MOBdir+"/"+Ndir+"/"+I)
    print(I)
    g1 = np.dot(imag1[...,:3], [0.2989, 0.5870, 0.1140])
    del imag1
    #g1 = abs(g01)
    rms=np.sqrt(np.mean(g1**2))
    #g1[g1 < rms * 3] = 0
    gmin = np.min(g1,initial = 100, where = (g1 > 0))
    gmax = np.max(g1)
    print("gmin",gmin)
    print("gmax",gmax)
    imin = np.where(g1 == gmin)
    #print("imin",imin)
    iixmin = imin[1][0]
    iiymin = imin[0][0]
    print("\n",ild,I,"rms=",rms,"\ngmin>0 = ",g1[iiymin][iixmin])

    #h0f = g1.flatten()
    #bi = int(gmax/g1[iiymin][iixmin])
    #plt.hist(h0f,bins = 700,log = True)
    #plt.show()

    coze0 = np.count_nonzero(g1)
    print("coze0",coze0)

    #iymi = max(0,iiymin-20)
    #iyma = min(g1.shape[0],iiymin+20)
    #ixmi = max(0,iixmin-20)
    #ixma = min(g1.shape[1],iixmin+20)

    g1[g1 < rms * 3] = 0
    #g1[g1 < 0.003] = 0
    coze = np.count_nonzero(g1)
    print("coze",coze)

    kernel = np.ones((3, 3))
    l, n = label(g1, structure=kernel)
    ind = [i for i in range(1,n+1,1)]
    su = sum_labels(g1, labels=l, index=ind)
    cm = center_of_mass(g1, labels=l, index=ind)
    lg = g1.copy()
    lg[lg > 0] = 1
    co = sum_labels(lg, labels=l, index=ind)
    #SU+=list(su)
    try:     print("n max(su) =",n,max(su))
    except: pass
    ar = [[ind[i],su[i],cm[i],co[i],I] for i in range(len(ind))]
    ra=sorted(ar,key=lambda ll:ll[1], reverse=True)
    print(ra[0])
    print(ra[-1])
    
    for i in range(len(ra)):
        if ra[i][1] < ot or ra[i][3] <3: break
        icmy = int(ra[i][2][0]+0.5)
        icmx = int(ra[i][2][1]+0.5)
        farg = str(icmy)+"|"+str(icmx)
        
        if not farg in PODC:
            iymi = max(0,icmy-20)
            iyma = min(g1.shape[0],icmy+20)
            ixmi = max(0,icmx-20)
            ixma = min(g1.shape[1],icmx+20)
            try:
                    a,b,D,DP, ro, R2,cmy,cmx = morph(g1[iymi:iyma,ixmi:ixma])
                    print("after morph a,b,ro R2:", a,b,ro, R2)
            except:
                    a = 0
                    ro = 0
            RA.append([ra[i][1],icmy,icmx,a,ro,I])
            if ra[i][1] > maxLX: maxLX = ra[i][1]

            if ild>2 :
                if 2<1:
                    tigmi = "%.4f"%(ra[i][1])+","+str(icmy)+","+str(icmx)+",%.2f"%(a)+",%.2f"%(ro)+","+str(I)
                    figmi = plt.figure(tigmi)
                    if math.fabs(a) <10: 
                        x=[cmx-5,cmx+5]
                        y=[a*x[0]+b,a*x[1]+b]
                        plt.plot(x,y,color='r')

                    plt.imshow(g1[iymi:iyma,ixmi:ixma])
                    if math.fabs(a) <10: 
                        x=[cmx-5,cmx+5]
                        y=[a*x[0]+b,a*x[1]+b]
                        plt.plot(x,y,color='r')
                    plt.show()
        try:
            PODC[farg] += 1            
        except:
            PODC[farg] = 1

    print("len(RA) = ",len(RA))

    #print(os.getpid(),psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    #print(psutil.virtual_memory())

  except: pass

print("len(RA)",len(RA))
ra = []
for i in range(len(RA)):
        farg = str(RA[i][1])+"|"+str(RA[i][2])
        if PODC[farg] == 1:
                ra.append(RA[i])
print("len(ra)",len(ra))        

RA=sorted(ra,key=lambda ll:ll[1], reverse=True)
LUXes = ""

with open("RA.csv","w") as fo:
  fo.write("lx|y|x|a|r|I\n")
  for i in range(min(10000,len(RA))):
    print("%0.4f"%(RA[i][0])+"|"+str(RA[i][1])+"|"+str(RA[i][2])+"|"+"%0.4f"%(RA[i][3])+"|"+"%0.4f"%(RA[i][4])+"|"+str(RA[i][5]))
    LUXes += " %0.4f"%(RA[i][0])
    fo.write("%0.4f"%(RA[i][0])+"|"+str(RA[i][1])+"|"+str(RA[i][2])+"|"+"%0.2f"%(RA[i][3])+"|"+"%0.2f"%(RA[i][4])+"|"+str(RA[i][5])+"\n")
with open("LU.txt","w") as fo:
    fo.write(str(Ndir)+" "+LUXes)
with open("NU.txt","w") as fo:
    fo.write(str(Ndir)+" "+ str(len(RA)) )#+" %0.4f"%(RA[0][0])+" %0.4f"%(RA[-1][0]))

try: os.makedirs(HODI+"RES"+CAMNO+"/"+str(Ndir))
except: pass

with open(HODI+"RES"+CAMNO+"/"+str(Ndir)+"/RA.csv","w") as fo:
  fo.write("lx|y|x|a|r|I\n")
  for i in range(min(10000,len(RA))):
    #print(RA[i])
    fo.write("%0.4f"%(RA[i][0])+"|"+str(RA[i][1])+"|"+str(RA[i][2])+"|"+"%0.2f"%(RA[i][3])+"|"+"%0.2f"%(RA[i][4])+"|"+str(RA[i][5])+"\n")
with open(HODI+"RES"+CAMNO+"/"+str(Ndir)+"/LU.txt","w") as fo:
    fo.write(str(Ndir)+" "+LUXes)
with open(HODI+"RES"+CAMNO+"/"+str(Ndir)+"/NU.txt","w") as fo:
    fo.write(str(Ndir)+" "+str(len(RA)))

