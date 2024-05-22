from ultralytics import YOLO
import cv2
from train import detect_number_plates
import os
img_path = "image/y.jpg"
try:
    with open(img_path, "rb") as f:
        pass
except FileNotFoundError:
    print(f"File {img_path} does not exist.")
    exit()
if __name__ == "__main__":
    model = YOLO(".train/best.pt")
    path = "./public/uploads/result/"
    file_path = path + "r.jpg"
    _, file_extension = os.path.splitext(file_path)
    if file_extension in [".jpg", ".jpeg", ".png"]:
        print("Processing the image...")

        image = cv2.imread(file_path)
        number_plate_list = detect_number_plates(image, model)
        cv2.imwrite(path + "output_image3.jpg", image)

