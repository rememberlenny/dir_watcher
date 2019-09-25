#!/bin/sh
# launcher.sh
# navigate to home directory, then to project directory, then execute python script, then back home

cd /home/pi/Spaceship/publicart
sleep 5
echo 'Starting main...'
sleep 5
python /home/pi/Spaceship/publicart/dir_watcher/main.py
