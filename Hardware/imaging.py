from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from picamera2 import Picamera2, Preview
import requests
from os import path
from io import BytesIO

gcs_url = 'http://192.168.1.64:80'

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # initalizing flask server

@app.route("/trigger_camera", methods={"POST"})
def trigger_camera():
    global Picamera2
    data = request.json

    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)
    picam2.start_preview(Preview.NULL)
    picam2.start()
    image_stream = BytesIO()
    image = picam2.capture_image('main')
    image.save(image_stream, format='JPEG')
    image_stream.seek(0)
    files = {
        'file': (f'capture.jpg', image_stream, 'images/jpeg'),
    }
    headers = {}
    response = requests.request("POST", f"{gcs_url}/submit", headers = headers, files = files)
    picam2.stop()
    return 'OK'
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

