# Directory Watcher

Work with instaloader to upload street art photos to publilcart

## What it does

This watches a folder used to crawl #streetart photos from instagram. The results of the downloaded files become stored in a folder, that then get uploaded to publicart.io

## Commands

Run the following in the parent folder of the `dir_watcher`. For example: `/project` and `/project/dir_watcher`.

`instaloader --login findpublicart --no-videos --no-compress-json --geotags "#streetart"`

## Important

- Make a `download-data.json` file in the module folder. ie. `/project/dir_watcher/download-data.json`
- Run the module from a root folder that is also running instaloader. For example, from `/project`, run `python dir_watcher/main.py`.
