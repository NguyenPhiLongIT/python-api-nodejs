import base64
from ultralytics import YOLO

# from easyocr import Reader
import time
import torch
import cv2
import os
import csv
import numpy as np

CONFIDENCE_THRESHOLD = 0.5
COLOR = (0, 255, 0)


def detect_number_plates(image, model, display=False):
    start = time.time()
    detections = model.predict(image)[0].boxes.data
    json = model.predict(image)[0].names

    print(detections)
    print("-----------")
    print("json", json)
    if detections.shape != torch.Size([0, 6]):
        boxes = []
        confidences = []
        classes = []
        classes_dic = model.predict(image)[0].names
        for detection in detections:
            print("detection:", detection)
            confidence = detection[4]
            if float(confidence) < CONFIDENCE_THRESHOLD:
                continue
            boxes.append(detection[:4])
            print("boxes", boxes)
            confidences.append(detection[4])
            classes.append(classes_dic[int(detection[5])])

        print(f"{len(boxes)} Number plate(s) have been detected.")
        number_plate_list = []
        for i in range(len(boxes)):
            xmin, ymin, xmax, ymax = (
                int(boxes[i][0]),
                int(boxes[i][1]),
                int(boxes[i][2]),
                int(boxes[i][3]),
            )
            number_plate_list.append(
                [[xmin, ymin, xmax, ymax], confidences[i], classes[i]]
            )
            print(number_plate_list[i])

        end = time.time()
        print(
            f"Time to detect the number plates: {(end - start) * 1000:.0f} milliseconds"
        )
        return number_plate_list
    else:
        print("No number plates have been detected.")
        return []
