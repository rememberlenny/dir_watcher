
import json
from tinydb import TinyDB, Query

from send_file_to_publicart import submit_image_and_get_id

db = TinyDB('dir_watcher/download-data.json')

previously_completed_art_name = ''
SESSION_COUNT = 0


def street_art_query(art_name):
    Art = Query()
    return (Art.name == art_name) & (Art.type == 'streetart')


def prepare_completed_image(completed_art_name):
    art_piece = db.search(street_art_query(completed_art_name))
    if (len(art_piece) > 0):
        completed_art_piece = art_piece[0]
        try:
            submit_image_and_get_id(completed_art_name)
        except Exception as e:
            print('what happened: ' + str(e))
            previously_completed_art_name = completed_art_name



def _check_modification(filename):
    global SESSION_COUNT
    SESSION_COUNT = SESSION_COUNT + 1
    print('CH: ' + filename)
    print('SC: ', SESSION_COUNT)


def update_db(art_name, type_data, event, type_bool):
    with open(event.src_path) as blob_data:
        # db.insert({
        #     'name': art_name,
        #     'type': type_data,
        #     'blob': blob_data})
        new_value_dict = {}
        new_value_dict[type_bool] = True
        db.update(new_value_dict, street_art_query(art_name))


def init_db_new_art(art_name):
    db.insert({'name': art_name, 'type': 'streetart', 'photo_count': 1, 'has_geo': False,
               'has_data': False, 'has_caption': False, 'was_uploaded': False})


def increment_photo_count(art_name, art_name_search):
    new_count = art_name_search[0]['photo_count'] + 1
    db.update({'photo_count': new_count}, street_art_query(art_name))


def is_data_blob(event):
    return event.src_path.find('.json') != -1


def is_caption_blob(event):
    return event.src_path.find('UTC.txt') != -1


def is_location_blob(event):
    return event.src_path.find('location.txt') != -1


def is_image(event):
    return event.src_path.find('.jpg') != -1


def add_image_record(art_name, new_count, event):
    db.insert({'name': art_name, 'type': 'image',
               'photo_id': new_count, 'file_path': event.src_path})
    print('Save image ', new_count)


def on_created_handler(event):
    global previously_completed_art_name
    new_count = 0

    # Get the image "name"
    file_name_base = event.src_path.split('/#streetart/')
    file_name_in_folder = file_name_base[1]
    file_name_without_extension = file_name_in_folder.split('_UTC')
    art_name = file_name_without_extension[0]

    if (art_name != previously_completed_art_name):
        prepare_completed_image(previously_completed_art_name)

    # Query for the name existing
    art_name_search = db.search(street_art_query(art_name))

    if (is_image(event)):
        # Check if the image exists in DB
        if (len(art_name_search) > 0):
            # If does exist, increase photo count
            increment_photo_count(art_name, art_name_search)

        else:
            # If doesn't exist, create base record
            init_db_new_art(art_name)

        # Add image record
        add_image_record(art_name, new_count, event)

    if (is_data_blob(event)):
        update_db(art_name, 'json_data', event, 'has_data')
        print('Save json')

    if (is_caption_blob(event)):
        update_db(art_name, 'caption_data', event, 'has_caption')
        print('Save caption')

    if (is_location_blob(event)):
        update_db(art_name, 'location_data', event, 'has_geo')
        print('Save location')
    
    previously_completed_art_name = art_name
    _check_modification(event.src_path)
