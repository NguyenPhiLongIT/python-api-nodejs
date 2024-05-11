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

import time

# Đặt ngưỡng độ tin cậy
CONFIDENCE_THRESHOLD = 0.5
# Màu của bounding box và văn bản
COLOR = (0, 255, 0)
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
    ls = data["data1"]
    filename = ls["filename"]
    code = ls["code"]
    decode_base64(filename, code)
    return json.dumps({"result": ls})


def process_image(imgdata):
    np_arr = np.frombuffer(
        imgdata, np.uint8
    )  # Convert base64-encoded image data to numpy array
    img = cv.imdecode(np_arr, cv.IMREAD_GRAYSCALE)
    _, binary_img = cv.threshold(img, 123, 250, cv.THRESH_BINARY_INV)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))
    img_dilate = cv.dilate(binary_img, kernel, anchor=(-1, -1), iterations=2)
    # img_erode = cv.erode(img_dilate, kernel)
    return img_dilate


def train(imgdata):
    np_arr = np.frombuffer(
        imgdata, np.uint8
    )  # Convert base64-encoded image data to numpy array
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    model = YOLO("yolov8n.pt")
    results = model(img, save=True)  # working
    print(results)
    res_plotted = results[0].plot()
    return res_plotted


def traindata(imgdata):
    np_arr = np.frombuffer(
        imgdata, np.uint8
    )  # Convert base64-encoded image data to numpy array
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    model = YOLO(".train/yolov8n.pt")
    model = YOLO(".train/best.pt")
    results = model.predict(img, save=True)  # working
    # cv.waitKey(1)
    res_plotted = results[0].plot()
    time.sleep(10)
    # cv.imwrite("dsd", res_plotted)
    return res_plotted


def predict(mode, base64_img):
    # Decode base64 string to bytes
    imgdata = base64.b64decode(base64_img)

    # Convert bytes to numpy array
    np_arr = np.frombuffer(imgdata, np.uint8)

    # Decode numpy array to image
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    combined_img = detect_number_plates(mode, img)
    return img


def predict1(img):
    yolov8_detector = YOLO(".train/best.pt")
    # Detect Objects
    boxes, scores, class_ids = yolov8_detector(img)

    # Draw detections
    combined_img = yolov8_detector.draw_detections(img)
    return combined_img


def decode_base64(filename, code):
    # imgdata = base64.b64decode(code)
    path = "../public/uploads/result/"
    directory = path + filename
    dir = directory[1:]

    # Giải mã chuỗi base64 thành dữ liệu nhị phân
    imgdata = base64.b64decode(code)

    # Chuyển dữ liệu nhị phân thành mảng NumPy
    np_arr = np.frombuffer(imgdata, np.uint8)

    # Đọc ảnh từ mảng NumPy
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)

    # Ghi ảnh vào file

    # with open(path, "wb") as f:
    #     # f.write(imgdata)
    #     # cv.imwrite(filename, img)
    #     cv.imwrite(filename, img)
    #     print("success")

    if not os.path.exists(path):
        os.makedirs(path)
    cv.imwrite(directory, img)
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
    number_plate_list = []
    for detection in arr:
        confidence = detection[1]
        if float(confidence) < CONFIDENCE_THRESHOLD:
            continue
        boxes.append(detection[:1])
        confidences.append(detection[1])

        # loop over the bounding boxes
        # for i in range(2):
        #     # extract the bounding box coordinates
        #     print(type(boxes[i][0][1]))
        #     xmin, ymin, xmax, ymax = (
        #         int(boxes[i][0][0]),
        #         int(boxes[i][0][1]),
        #         int(boxes[i][0][2]),
        #         int(boxes[i][0][3]),
        #     )
        #     # append the bounding box of the number plate
        #     number_plate_list.append([[xmin, ymin, xmax, ymax], confidences[i]])
        # print(xmin, ymin, xmax, ymax, confidences)
        # image = cv.imread(directory)
        # img = np.array(image)
        # cv.rectangle(img, (274, 258), (341, 328), COLOR, 3)
        # text = "Number Plate: {:.2f}%".format(0.9932 * 100)
        # print("rectangle")
        # cv.putText(
        #     directory, text, (274, 258 - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2
        # )

        print("successful")
    image = cv.imread(directory)
    cv.putText(image, "dfff", (274, 258 - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2)
    cv.imwrite(directory, image)
    


# def decode_base64(filename, code):

#     imgdata = base64.b64decode(code)
#     filename = "./public/uploads/result/" + filename
#     modelPath = ".train/best.pt"
# with open(filename, "wb") as f:
#     result = predict(modelPath, imgdata)
#     if result is not None:
#         cv.imwrite(filename, result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    app.run(port=port, debug=True, use_reloader=False)
    print()
