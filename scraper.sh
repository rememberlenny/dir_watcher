#!/bin/sh
# scraper.sh
# kick off the instaloader task

cd ~/
cd ~/Spaceship/publicart
workon insta
instaloader --login streetarrrrt --no-videos --no-compress-json --geotags "#streetart"
