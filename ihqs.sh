#!/bin/bash
#python3 /home/madiz/rdl.py  NU.txt LU.txt RA.csv
HOD0=/home/madiza/MOB0
HOD1=/home/madiza/MOB1
python3 /home/madiza/rdl.py
mkdir $HOD0
mkdir $HOD1
dn=$(ls $HOD0 | wc -l)
mkdir $HOD0/$dn
mkdir $HOD1/$dn
for i in $(seq 1 20);
do
    echo $i
    date +%T
    python3 /home/madiza/ooo.py 0 $dn &
    python3 /home/madiza/ooo.py 1 $dn &
    sleep 10
done
python3 /home/madiza/1.py 0 $dn
python3 /home/madiza/1.py 1 $dn
python3 /home/madiza/2.py
python3 /home/madiza/rdl.py # NU.txt LU.txt RA.csv
date +%T
