import sys
import time
import logging
import json
import requests
import os
import shutil
import glob
import boto3
import instaloader
from pathlib import Path
from redis import Redis
from rq import Queue
from botocore.exceptions import ClientError
from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
from multiprocessing import Process
from tinydb import TinyDB, Query

print('Starting monitoring tool')

import os

dirpath = os.getcwd()
foldername = os.path.basename(dirpath)

HOME_DIR = dirpath

IS_PROD = False
APP_PATH_ROOT = HOME_DIR
APP_SCRIPT_PATH = APP_PATH_ROOT
S3_BUCKET_NAME = 'publicart-indexer'
LOCAL_DB_FILE_NAME = 'database-data.json'
INSTAGRAM_USER_NAME = 'streetarrrrt'
INSTAGRAM_USER_PAME = 'password123!'
INSTAGRAM_INDEX_HASHTAG = 'streetart'
INSTAGRAM_SESSION_LOCATION = APP_PATH_ROOT + 'pwd/.instaloader-session'
LOCAL_DB_LOCATION = APP_PATH_ROOT + LOCAL_DB_FILE_NAME
IS_PROD = True

print(APP_PATH_ROOT)

HASHTAG = 'streetart'
BUCKET_NAME = 'publicart-indexer'
OBJECT_PATH = 'pa-rpi1-indexer/'
FILE_NAME = 'test.txt'
LOCAL_DB_FILE_NAME = LOCAL_DB_FILE_NAME if LOCAL_DB_FILE_NAME else ""
APP_SCRIPT_PATH = APP_SCRIPT_PATH if APP_SCRIPT_PATH else ""
INSTAGRAM_INDEX_HASHTAG = INSTAGRAM_INDEX_HASHTAG if INSTAGRAM_INDEX_HASHTAG else ""

previously_completed_art_name = ''
SESSION_COUNT = 0

IS_PROD = True
PROD_URL = 'https://www.publicart.io'
STAG_URL = 'https://publicart-site-staging.herokuapp.com'
ROOT_URL = PROD_URL if IS_PROD else STAG_URL
IMAGE_ROOT_PATH = './#' + HASHTAG + '/'
LOCATION_POST_FIX = '_location.txt'
JPG_POST_FIX = '.jpg'
LOCATION_UTC_POST_FIX = '_UTC' + LOCATION_POST_FIX
API_URL = ROOT_URL + '/pictures?no_partial=1'
METADATA_URL = ROOT_URL + '/pictures/metadata'
GENERIC_HEADER = {'Content-type': 'multipart/form-data'}
GOOGLE_MAPS_URL_BASE = 'https://maps.google.com/maps?q='
TRANSFERED_ART_DIR = 'transfered_' + HASHTAG
DEFAULT_ART_DIR = '#' + HASHTAG


def delete_folder(media_id):
    shutil.rmtree(APP_PATH_ROOT + '/images/' + str(media_id))
    print('Deleted ' + str(media_id))

def after_submit_image_get_id(r):
    json_data = json.loads(r.text)
    picture_id = json_data['picture_id']
    return picture_id


def get_date_from_name(date):
    return date.strftime("%m-%d-%Y_%H-%M-%S")



def generate_metadata(picture_id, data):
    # pprint(data)
    r = requests.post(METADATA_URL, data=data)
    # r = requests.post(api_url, files=files, data=data, headers=headers)
    # print(r.text)



def submit_image_and_get_id(media_id, date, location):
    art_piece_images = glob.glob(HOME_DIR + '/images/' + str(media_id) + '/*.jpg')
    date_of_image = get_date_from_name(date)

    length = len(art_piece_images)
    print('Images total ' + str(length))
    for i in range(length):
        print('Uploading ' + str(i))
        file_path = art_piece_images[i]
        print(art_piece_images[i])

        files = {'file': open(file_path, 'rb')}
        file_response = requests.post(API_URL, files=files)
        print('response ', file_response)
        picture_id = after_submit_image_get_id(file_response)

        # data = {"location_name": location_name, "file_name": art_name, "latitude": latlon[0], "longitude": latlon[1]}
        data = {"date_of_image": date_of_image, "location_name": location.name, "file_name": media_id,
                "latitude": location.lat, "longitude": location.lng, "picture_id": picture_id}
        generate_metadata(picture_id, data)

    delete_folder(media_id)



def upload_file(file_name):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then same as file_name
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, BUCKET_NAME, OBJECT_PATH + file_name)
    except ClientError as e:
        print(str(e))
        return False
    return True

def index_images():
    L = instaloader.Instaloader(download_videos=False, compress_json=False)
    L.login(INSTAGRAM_USER_NAME, INSTAGRAM_USER_PAME)
    print('Indexing started')
    for post in L.get_hashtag_posts(HASHTAG):
        # post is an instance of instaloader.Post
        if post.location is not None:
            was_downloaded = L.download_post(post, target=Path('images/', str(post.mediaid)) )
            submit_image_and_get_id(post.mediaid, post.date, post.location)

index_images()