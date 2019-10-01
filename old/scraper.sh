#!/bin/sh
# scraper.sh
# kick off the instaloader task

export DEVICE_NAME='RPI-STREETART'
export INSTAGRAM_USER_NAME='streetarrrrt'
export INSTAGRAM_INDEX_HASHTAG='streetart'

source /home/pi/instaloader/bin/activate 

cd /home/pi/
cd /home/pi/Spaceship/publicart/

echo 'Starting in 20 seconds'

sleep 10
echo 'Starting in 10 seconds'

sleep 5
echo 'Starting in 5...'

sleep 5
echo 'Running instaloader'

python /home/pi/Spaceship/publicart/dir_watcher/main.py & sh -c 'instaloader --login ${0} --sessionfile /home/pi/Spaceship/publicart/pwd/.instaloader-session  --no-videos --no-compress-json --geotags "#${1}"' "$INSTAGRAM_USER_NAME" "$INSTAGRAM_INDEX_HASHTAG"
