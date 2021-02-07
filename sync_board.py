import pickle

import cv2
import requests, time
import numpy as np
import base64
from threading import Thread

class SyncableBoard:
    def __init__(self, url):
        self.url = url
        self.running = False
        self.sync_runner = None
        self._array = None
    @property
    def array(self):
        return self._array

    def set_array(self, array):
        self._array = array
    def start_syncing(self):
        self.running = True
        self.sync_runner = Thread(target=self.sync_thread, daemon=True)
        self.sync_runner.start()

    def stop_syncing(self):
        self.running = False
        self.sync_runner.join()

    def sync_thread(self):
        old_state = self._array.copy()
        last_check_time = time.time()
        print('boop')
        while self.running:
            if time.time() - last_check_time > 0.1:
                new_data = requests.get(self.url)
                received_data = pickle.loads(base64.urlsafe_b64decode(new_data.text))
                old_mask = cv2.bitwise_not(cv2.inRange(self._array, (0, 0, 0), (0, 0, 0))) # all pixels that are not "transparent"
                new_mask = cv2.bitwise_not(cv2.inRange(received_data, (0, 0, 0), (0, 0, 0))) # all pixels that are not "transparent"
                new_pixels_keep_mask = cv2.bitwise_and(cv2.bitwise_not(old_mask), new_mask)
                old_pixels_keep_mask = cv2.bitwise_and(old_mask, cv2.bitwise_not(new_mask))
                old_pixels_keep = cv2.bitwise_and(self._array, self._array, dst=self._array, mask=old_pixels_keep_mask)
                new_pixels_keep = cv2.bitwise_and(received_data, received_data, mask=new_pixels_keep_mask)
                self._array += new_pixels_keep
                if not np.array_equal(old_state, received_data):
                    post = requests.post(self.url+"/update", base64.urlsafe_b64encode(self._array.dumps()))
                last_check_time = time.time()
                old_state = self._array.copy()
            else:
                time.sleep(0.1)

