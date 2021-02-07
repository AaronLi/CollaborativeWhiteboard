import pickle
import base64
from flask import Flask, request
import numpy as np
import cv2
app = Flask(__name__)

data = np.zeros((480, 640, 3), dtype=np.uint8)

@app.route('/')
def get_data():
    global data
    return base64.urlsafe_b64encode(data.dumps())

@app.route('/update', methods=('POST',))
def put_data():
    global data
    new_data = pickle.loads(base64.urlsafe_b64decode(request.data))
    data = new_data
    return 'ok'

if __name__ == '__main__':
    app.run("0.0.0.0")