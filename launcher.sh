#!/bin/sh
# launcher.sh
# navigate to home directory, then to project directory, then execute python script, then back home

which python
source /home/pi/.bashrc 
which python
cd /home/pi/Spaceship/publicart/dir_watcher
cd /home/pi/Spaceship/publicart
python dir_watcher/main.py

