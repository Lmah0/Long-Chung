# Server that listens for queries from the website/app side
from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS
import requests
import json
import glob
import sys

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.post('/submit/')
def submit_data():
    file = request.files["file"] #file must be attached in body with name "file"
    file.save('/Users/sauceke/Documents/GitHub/Surveillance-System/Website/backend/images/' + file.filename) #saves the image
    print('Saved file', file.filename)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80) # recieving the image

# trigger the server on the pi
