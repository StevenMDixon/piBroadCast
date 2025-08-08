#/usr/bin/bash

cd ~/PiBroadcast
. env/bin/activate

python3 server.py 1>/dev/null 2>/dev/null & disown