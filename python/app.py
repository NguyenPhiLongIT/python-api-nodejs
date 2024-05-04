import os
import flask
import subprocess
import json
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import base64
import cv2 as cv
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Flask server"

@app.route("/pyserver/<image_path>", methods=['GET'])
def call_python(image_path):
    print("image path", image_path )
    subprocess.Popen(
        ['python', 'main.py',image_path],
    )
    return '1'

@app.route('/postdata', methods=['POST'])
def postdata():
    data = request.get_json() 
    print(data)
    ls = data['data1']
    filename = ls['filename']
    code = ls['code']
    decode_base64(filename, code)
    return json.dumps({"result":ls}) 

def process_image(imgdata):
    np_arr = np.frombuffer(imgdata, np.uint8)   # Convert base64-encoded image data to numpy array
    img = cv.imdecode(np_arr, cv.IMREAD_GRAYSCALE)
    _, binary_img = cv.threshold(img, 123, 250, cv.THRESH_BINARY_INV)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7,7))
    img_dilate = cv.dilate(binary_img, kernel, anchor=(-1, -1), iterations=2)
    # img_erode = cv.erode(img_dilate, kernel)

    return img_dilate

def train(imgdata):
    np_arr = np.frombuffer(imgdata, np.uint8)   # Convert base64-encoded image data to numpy array
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    model = YOLO('yolov8n.pt')
    results = model(img, save=True)  # working
    print(results)
    cv.waitKey(1)
    res_plotted = results[0].plot()
    return res_plotted

def decode_base64(filename, code):
    imgdata = base64.b64decode(code)
    filename = '../public/uploads/result/' + filename
    # with open(filename, 'wb') as f:
    #     result = process_image(imgdata)
    #     cv.imwrite(filename, result)
    with open(filename, 'wb') as f:
        result = train(imgdata)
        cv.imwrite(filename, result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, debug=True, use_reloader=False)
	
    