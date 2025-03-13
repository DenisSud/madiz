#!/bin/bash

for i in $(seq 1 480);
do
    echo $i
    sleep 1
    /home/madiza/ihqs.sh
done
