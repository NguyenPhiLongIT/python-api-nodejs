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
from train import detect_number_plates
import math

import time

# Đặt ngưỡng độ tin cậy
CONFIDENCE_THRESHOLD = 0.5
# Màu của bounding box và văn bản
COLOR = (54, 12, 92)
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Flask server"


@app.route("/pyserver/<image_path>", methods=["GET"])
def call_python(image_path):
    print("image path", image_path)
    subprocess.Popen(
        ["python", "main.py", image_path],
    )
    return "1"


@app.route("/postdata", methods=["POST"])
def postdata():
    data = request.get_json()
    print(data)
    arr = []
    ls = data["data1"]
    print("ls", ls)
    filename = ls["filename"]
    code = ls["code"]
    decode_base64(filename, code, arr)
    # ls["angle_now"] = arr[0]
    ls["angle_now"] = 666
    print("angle_now", ls["angle_now"])
    print("angle-now: ", ls["angle_now"])
    print("aaeddd", arr)
    # ls["angle_result"] = arr[1]
    ls["angle_result"] = 666
    decode_base64(filename, code, arr)
    print("postdata")
    return json.dumps({"result": ls})


def decode_base64(filename, code, arr):
    path = "../public/uploads/"
    directory = path + filename
    result_dir = "../public/uploads/result/" + filename
    imgdata = base64.b64decode(code)
    np_arr = np.frombuffer(imgdata, np.uint8)
    imdecode_img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    image = imdecode_img.copy()
    # if not os.path.exists(path):
    #     os.makedirs(path)
    # cv.imwrite(directory, img)
    print("Image saved successfully.")
    print(dir)
    print(directory)
    modelPath = ".train/best.pt"
    if not os.path.exists(modelPath):
        os.makedirs(modelPath)
        print("no path")

    model = YOLO(modelPath)

    print("processing-----------")
    arr = detect_number_plates(directory, model)
    print("processing")
    print(arr)
    confidences = []
    boxes = []
    classes = []
    number_plate_list = []
    centers = []
    for detection in arr:
        confidence = detection[1]
        if float(confidence) < CONFIDENCE_THRESHOLD:
            continue
        boxes.append(detection[0])
        confidences.append(confidence)
        classes.append(detection[2])
        xmin = detection[0][0]
        ymin = detection[0][1]
        xmax = detection[0][2]
        ymax = detection[0][3]

        center1 = math.sqrt(pow(xmax - xmin, 2) + pow(ymax - ymin, 2)) / 2.0
        center2 = (xmax - xmin) / 2.0
        centers.append(center1)
        centers.append(center2)

        print(xmin, ymin, xmax, ymax, confidence, detection[2])
        # image = cv.imread(directory)
        cv.rectangle(image, (xmin, ymin), (xmax, ymax), COLOR, 2)
        text = "{}: {:.2f}%".format(detection[2], confidence * 100)
        cv.putText(
            image, text, (xmin, ymin - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2
        )
        cv.imwrite(result_dir, image)

        print("successful")
    if centers[0] > centers[2]:
        angle = np.arctan((xmax - xmin) / (ymax - ymin))
        angle_now = -1 * (angle + 90)
        angle_return = angle_now + 45
    elif centers[0] < centers[2]:
        angle = np.arctan((xmax - xmin) / (ymax - ymin))
        angle_now = 90 - angle
        angle_return = 45 - angle_now
    else:
        angle_now = -90
        angle_return = 45
    result = []
    result.append(angle_now)
    result.append(angle_return)
    arr = result
    print("arr:", arr)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    app.run(port=port, debug=True, use_reloader=False)
    print()
