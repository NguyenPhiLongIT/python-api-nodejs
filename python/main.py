import flask
import cv2
import sys
import os
import time 

def read_images_from_directory(directory_path):
    images = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory_path, filename)
            image = cv2.imread(image_path)
            if image is not None:
                print("Đã đọc ảnh từ:", image_path)
                images.append(image)
            else:
                print("Không thể đọc ảnh từ:", image_path)
    return images
new_frame_time = time.time()
