#!/bin/sh
# scraper.sh
# kick off the instaloader task

source /home/pi/instaloader/bin/activate 
cd /home/pi/
cd /home/pi/Spaceship/publicart/

instaloader --login streetarrrrt --sessionfile /home/pi/Spaceship/publicart/pwd/.instaloader-session  --no-videos --no-compress-json --geotags "#streetart"
