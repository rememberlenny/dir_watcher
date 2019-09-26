import sys
import time
import logging
import json
import requests

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from on_created_handler import on_created_handler
from set_local_envs import setup_env_vars

print('Starting monitoring tool')

class _CustomHandler(FileSystemEventHandler):
    def on_created(self, event):
        try:
            on_created_handler(event)
        except Exception as e:
    	    print('Error: '+ str(e)) 


if __name__ == "__main__":
    setup_env_vars()
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = _CustomHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
