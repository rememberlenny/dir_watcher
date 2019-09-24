import sys
import time
import logging
import json
import requests
import os
import shutil
import glob

from pathlib import Path
from redis import Redis
from rq import Queue
from tinydb import TinyDB, Query

q = Queue(connection=Redis())
db = TinyDB('dir_watcher/download-data.json')

IS_PROD = True
PROD_URL = 'https://www.publicart.io'
STAG_URL = 'https://publicart-site-staging.herokuapp.com'
ROOT_URL = PROD_URL if IS_PROD else STAG_URL
IMAGE_ROOT_PATH = './#streetart/'
LOCATION_POST_FIX = '_location.txt'
JPG_POST_FIX = '.jpg'
LOCATION_UTC_POST_FIX = '_UTC' + LOCATION_POST_FIX
API_URL = ROOT_URL + '/pictures?no_partial=1'
METADATA_URL = ROOT_URL + '/pictures/metadata'
GENERIC_HEADER = {'Content-type': 'multipart/form-data'}
GOOGLE_MAPS_URL_BASE = 'https://maps.google.com/maps?q='
TRANSFERED_ART_DIR = 'transfered_streetart'
DEFAULT_ART_DIR = '#streetart'

def move_files_to_old_folder(art_name):
    art_name_related_files = glob.glob('./#streetart/' + art_name + '*')
    length = len(art_name_related_files)
    for i in range(length):
        new_path = art_name_related_files[i].replace(
            DEFAULT_ART_DIR, TRANSFERED_ART_DIR)
        print('Moved ' + new_path)
        shutil.move(art_name_related_files[i], new_path)


def after_submit_image_get_id(r):
    json_data = json.loads(r.text)
    picture_id = json_data['picture_id']
    return picture_id


def get_date_from_name(name):
    name_of_file_parts = name.split('_')
    date_of_image = name_of_file_parts[0]
    return date_of_image


def generate_metadata(picture_id, data):
    # pprint(data)
    r = requests.post(METADATA_URL, data=data)
    # r = requests.post(api_url, files=files, data=data, headers=headers)
    # print(r.text)


def get_location_details(file_path):
    with open(file_path) as f:
        lines = f.readlines()
        location_name = lines[0]
        latlongquery = lines[1].split(GOOGLE_MAPS_URL_BASE)
        latlongblock = latlongquery[1].split('&ll=')
        latlonpoints = latlongblock[0].split(',')
        #     latitude = latlonpoints[0]
        #     longitude = latlonpoints[1]
        return [location_name, latlonpoints]


def submit_image_and_get_id(art_name):
    potential_location_file = IMAGE_ROOT_PATH + art_name + LOCATION_UTC_POST_FIX
    my_file = Path(potential_location_file)

    if my_file.is_file():
        [location_name, latlon] = get_location_details(potential_location_file)
        date_of_image = get_date_from_name(art_name)
        image_file_name = potential_location_file.replace(
            LOCATION_POST_FIX, JPG_POST_FIX)
        
        Art = Query()
        art_piece_images = db.search((Art.name == art_name) & (Art.type == 'image'))
        
        length = len(art_piece_images) 
        for i in range(length): 
                file_path = art_piece_images[i]['file_path']
                print(art_piece_images[i]['file_path']) 

                files = {'file': open(file_path, 'rb')}
                file_response = requests.post(API_URL, files=files)
                picture_id = after_submit_image_get_id(file_response)

                # data = {"location_name": location_name, "file_name": art_name, "latitude": latlon[0], "longitude": latlon[1]}
                data = {"date_of_image": date_of_image, "location_name": location_name, "file_name": art_name,
                        "latitude": latlon[0], "longitude": latlon[1], "picture_id": picture_id}
                generate_metadata(picture_id, data)

                completed_upload(art_name)
        for i in range(length):
                move_files_to_old_folder(completed_art_name)

def completed_upload(completed_art_name):
    Art = Query()
    db.update({'was_uploaded': True}, ((Art.name == completed_art_name) & (Art.type == 'streetart')))
    print('Piece uploaded: ' + completed_art_name)
