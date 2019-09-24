#!/bin/sh
# scraper.sh
# kick off the instaloader task

cd ~/
cd ~/Spaceship/publicart
source /home/pi/insta/bin/activate
instaloader --login streetarrrrt --no-videos --no-compress-json --geotags "#streetart"
