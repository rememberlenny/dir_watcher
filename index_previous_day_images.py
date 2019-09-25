from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

USERNAME = 'streetarrrrt'
FILENAME = '/home/pi/Spaceship/publicart/pwd/.instaloader-session'

L = instaloader.Instaloader(download_pictures=True, download_comments=False, download_videos=False, download_geotags=True, save_metadata=True, compress_json=False)
L.load_session_from_file(USERNAME, FILENAME)

posts = L.get_hashtag_posts('streetart')

SINCE = datetime(2019, 9, 2)
UNTIL = datetime(2019, 9, 23)

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    print(post.date_utc)
    L.download_post(post, '#test-streetart/')
