import os

from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

USERNAME = os.environ['INSTAGRAM_USER_NAME']
FILENAME = os.environ['INSTAGRAM_SESSION_LOCATION']
HASHTAG = os.environ['INSTAGRAM_INDEX_HASHTAG']

L = instaloader.Instaloader(download_pictures=True, download_comments=False, download_videos=False, download_geotags=True, save_metadata=True, compress_json=False)
L.load_session_from_file(USERNAME, FILENAME)

posts = L.get_hashtag_posts(HASHTAG)

SINCE = datetime(2019, 9, 2)
UNTIL = datetime(2019, 9, 23)

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    print(post.date_utc)
    L.download_post(post, '#test-streetart/')
