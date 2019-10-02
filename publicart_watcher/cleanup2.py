import time
import json
import requests
import shutil
import glob
import os

print('Starting monitoring tool')

dirpath = os.getcwd()
foldername = os.path.basename(dirpath)

HOME_DIR = dirpath
APP_ROOT = '/home/lkbgift/Spaceship/datasets'

APP_PATH_ROOT = HOME_DIR
APP_SCRIPT_PATH = APP_PATH_ROOT
HASHTAG = 'streetart'
INSTAGRAM_USER_NAME = 'streetarrrrt'
INSTAGRAM_USER_PAME = 'password123!'
INSTAGRAM_INDEX_HASHTAG = HASHTAG
IS_PROD = True

print(APP_PATH_ROOT)

previously_completed_art_name = ''

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



def delete_files(time_stamp):
    print('Running delete')
    art_piece_images = glob.glob(APP_ROOT + '/#' + HASHTAG + '/' + time_stamp + '*')
    length = len(art_piece_images)
    print('Deleting total ' + str(length))
    for i in range(length):
        print('Deleting ' + str(i) + ' of ' + str(length))
        os.remove(art_piece_images[i])
        print('Delete confirmed ' + str(art_piece_images[i]))


def after_submit_image_get_id(r):
    json_data = json.loads(r.text)
    picture_id = json_data['picture_id']
    return picture_id


def generate_metadata(picture_id, data):
    r = requests.post(METADATA_URL, data=data)


def upload_file_to_publicart(file_path, date_of_image, location_name, art_name, latlon):
    files = {'file': open(file_path, 'rb')}
    file_response = requests.post(API_URL, files=files)

    print('response ', file_response)
    if file_response.ok:
        print('success ', file_path)
        picture_id = after_submit_image_get_id(file_response)
        print('picture_id ', str(picture_id))

        # data = {"location_name": location_name, "file_name": art_name, "latitude": latlon[0], "longitude": latlon[1]}
        data = {"date_of_image": date_of_image, "location_name": location_name, "file_name": art_name,
                "latitude": latlon[0], "longitude": latlon[1], "picture_id": picture_id}
        generate_metadata(picture_id, data)
    else:
        print('issue ', file_path)
        time.sleep(15)
        upload_file_to_publicart(file_path, date_of_image, location_name, art_name, latlon)


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


def get_date_from_name(name):
    name_of_file_parts = name.split('_')
    date_of_image = name_of_file_parts[0]
    return date_of_image


def submit_image_and_get_id(location_path):
    [location_name, latlon] = get_location_details(location_path)
    # media_id, date, location
    date = location_path.split(HASHTAG + '/')[1]
    date_of_image = get_date_from_name(date)
    time_stamp = date.split('_UTC')[0]
    art_piece_images = glob.glob(APP_ROOT + '/#' + HASHTAG + '/' + time_stamp + '*.jpg')
    json_path = location_path.replace('_location.txt', '.json')
    with open(json_path) as json_file:
        data = json.load(json_file)
    art_name = data['node']['id']

    length = len(art_piece_images)
    print('Images total ' + str(length) + ' for ' + date_of_image)
    for i in range(length):
        print('Uploading ' + str(i) + ' of ' + str(length))
        file_path = art_piece_images[i]
        print(art_piece_images[i])
        upload_file_to_publicart(file_path, date_of_image, location_name, art_name, latlon)

    delete_files(time_stamp)


def cleanup_images():
    file_path_string = APP_ROOT + '/#' + HASHTAG + '/*' + LOCATION_POST_FIX
    print('Searching '+ file_path_string)

    location_images = glob.glob(file_path_string)

    print('Starting clean up ' + str(len(location_images)))
    length = len(location_images)
    for i in range(length):
        print('Cleanup ' + str(i) + " of " + str(length))
        location_path = location_images[i]
        submit_image_and_get_id(location_path)


cleanup_images()
