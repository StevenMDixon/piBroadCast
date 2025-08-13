#!/usr/bin/bash

sleep 10
sudo mount.cifs //Laptop-Base-Station/d /home/piratestation/nick -o user=user,password=1

cd /home/piratestation/Desktop/piBroadCast/ 
. env/bin/activate

python3 server.py
