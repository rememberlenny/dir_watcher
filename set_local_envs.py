import os

def setup_env_vars():
# Set environment variables
os.environ['APP_PATH_ROOT'] = '/home/pi/Spaceship/publicart'
os.environ['APP_SCRIPT_PATH'] = os.environ['APP_PATH_ROOT'] + '/dir_watcher/'
os.environ['DEVICE_NAME'] = os.getenv('DEVICE_NAME') if os.getenv('DEVICE_NAME') else 'RPI-STREETART'
os.environ['S3_BUCKET_NAME'] = 'publicart-indexer'
os.environ['LOCAL_DB_FILE_NAME'] = 'database-data.json'
os.environ['INSTAGRAM_USER_NAME'] = os.getenv('INSTAGRAM_USER_NAME') if os.getenv('INSTAGRAM_USER_NAME') else 'streetarrrrt'
os.environ['INSTAGRAM_INDEX_HASHTAG'] = os.getenv('INSTAGRAM_INDEX_HASHTAG') if os.getenv('INSTAGRAM_INDEX_HASHTAG') else 'streetart'
os.environ['INSTAGRAM_SESSION_LOCATION'] = os.environ['APP_PATH_ROOT'] + '/pwd/.instaloader-session'
