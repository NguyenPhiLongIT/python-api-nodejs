from ultralytics import YOLO
import cv2
model=YOLO('yolov8n.pt')
results=model('./images/21kg/2024_04_25_12h47m09_N2 21kg_OK.jpeg', show=True)
cv2.waitKey(0)
