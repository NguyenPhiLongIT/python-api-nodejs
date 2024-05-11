import base64
from ultralytics import YOLO

# from easyocr import Reader
import time
import torch
import cv2
import os
import csv


CONFIDENCE_THRESHOLD = 0.4
COLOR = (0, 255, 0)


import cv2
import numpy as np
import torch
import time

# Đặt ngưỡng độ tin cậy
CONFIDENCE_THRESHOLD = 0.5
# Màu của bounding box và văn bản
COLOR = (0, 255, 0)


# def detect_number_plates(base64_image, model, display=False):
#     start = time.time()
#     # Chuyển đổi mã base64 thành dữ liệu ảnh
#     image_data = base64.b64decode(base64_image)
#     nparr = np.frombuffer(image_data, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Chuyển ảnh sang định dạng tensor
#     # image_tensor = torch.from_numpy(image).unsqueeze(0)

#     # Truy vấn model để nhận dự đoán
#     detections = model.predict(image)[0].boxes.data

#     # Kiểm tra xem có phát hiện nào không
#     if detections.shape != torch.Size([0, 6]):
#         # Khởi tạo danh sách bounding boxes và độ tin cậy
#         boxes = []
#         confidences = []

#         # Lặp qua các dự đoán
#         for detection in detections:
#             # Trích xuất độ tin cậy
#             confidence = detection[4]

#             # Lọc ra các dự đoán yếu bằng cách đảm bảo độ tin cậy lớn hơn ngưỡng
#             if float(confidence) < CONFIDENCE_THRESHOLD:
#                 continue

#             # Nếu độ tin cậy lớn hơn ngưỡng, thêm bounding box và độ tin cậy vào danh sách tương ứng
#             boxes.append(detection[:4])
#             confidences.append(detection[4])

#         print(f"{len(boxes)} Number plate(s) have been detected.")
#         # Khởi tạo danh sách để lưu bounding boxes của biển số xe
#         number_plate_list = []

#         # Lặp qua các bounding boxes
#         for i, (box, confidence) in enumerate(zip(boxes, confidences)):
#             # Trích xuất tọa độ bounding box
#             xmin, ymin, xmax, ymax = (
#                 int(box[0]),
#                 int(box[1]),
#                 int(box[2]),
#                 int(box[3]),
#             )
#             # Thêm bounding box của biển số xe vào danh sách
#             number_plate_list.append([[xmin, ymin, xmax, ymax], confidence])

#             # In ra tọa độ của bounding box
#             print(f"Bounding box {i + 1}: [{xmin}, {ymin}, {xmax}, {ymax}]")

#             # Vẽ bounding box và nhãn lên ảnh
#             cv2.rectangle(image, (xmin, ymin), (xmax, ymax), COLOR, 3)
#             text = "Number Plate: {:.2f}%".format(confidence * 100)
#             cv2.putText(
#                 image, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2
#             )

#             if display:
#                 # Cắt ảnh vùng biển số xe được phát hiện
#                 number_plate = image[ymin:ymax, xmin:xmax]
#                 # Hiển thị biển số xe
#                 cv2.imshow(f"Number plate {i}", number_plate)

#         end = time.time()
#         # Hiển thị thời gian phát hiện biển số xe
#         print(
#             f"Time to detect the number plates: {(end - start) * 1000:.0f} milliseconds"
#         )
#         # Trả về danh sách chứa bounding boxes của biển số xe
#         return number_plate_list
#     # Nếu không có dự đoán, hiển thị thông báo
#     else:
#         print("No number plates have been detected.")
#         return []


def detect_number_plates(image, model, display=False):
    start = time.time()
    detections = model.predict(image)[0].boxes.data

    # detect = model.predict(image)[0].classes.data
    json = model.predict(image)[0].masks

    print(detections)
    print("-----------")
    print(json)
    if detections.shape != torch.Size([0, 6]):
        boxes = []
        confidences = []
        for detection in detections:
            confidence = detection[4]
            if float(confidence) < CONFIDENCE_THRESHOLD:
                continue
            boxes.append(detection[:4])
            confidences.append(detection[4])

        print(f"{len(boxes)} Number plate(s) have been detected.")
        number_plate_list = []
        for i in range(len(boxes)):
            xmin, ymin, xmax, ymax = (
                int(boxes[i][0]),
                int(boxes[i][1]),
                int(boxes[i][2]),
                int(boxes[i][3]),
            )
            # append the bounding box of the number plate
            number_plate_list.append([[xmin, ymin, xmax, ymax], confidences[i]])
            print(number_plate_list[i])
            # image = cv2.imread(image)
            # # draw the bounding box and the label on the image
            # cv2.rectangle(image, (xmin, ymin), (xmax, ymax), COLOR, 3)
            # text = "Number Plate: {:.2f}%".format(confidences[i] * 100)
            # cv2.putText(
            #     image, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2
            # )

            # if display:
            #     # crop the detected number plate region
            #     number_plate = image[ymin:ymax, xmin:xmax]
            # display the number plate
            # cv2.imshow(f"Number plate {i}", number_plate)

        end = time.time()
        # show the time it took to detect the number plates
        print(
            f"Time to detect the number plates: {(end - start) * 1000:.0f} milliseconds"
        )
        # return the list containing the bounding
        # boxes of the number plates
        return number_plate_list
    # if there are no detections, show a custom message
    else:
        print("No number plates have been detected.")
        return []


# def detect_number_plates(image, model, display=False):
#     start = time.time()
#     # pass the image through the model and get the detections
#     detections = model.predict(image)[0].boxes.data

#     # check to see if the detections tensor is not empty
#     if detections.shape != torch.Size([0, 6]):

#         # initialize the list of bounding boxes and confidences
#         boxes = []
#         confidences = []

#         # loop over the detections
#         for detection in detections:
#             # extract the confidence (i.e., probability) associated
#             # with the prediction
#             confidence = detection[4]

#             # filter out weak detections by ensuring the confidence
#             # is greater than the minimum confidence
#             if float(confidence) < CONFIDENCE_THRESHOLD:
#                 continue

#             # if the confidence is greater than the minimum confidence, add
#             # the bounding box and the confidence to their respective lists
#             boxes.append(detection[:4])
#             confidences.append(detection[4])

#         print(f"{len(boxes)} Number plate(s) have been detected.")
#         # initialize a list to store the bounding boxes of the
#         # number plates and later the text detected from them
#         number_plate_list = []

#         # loop over the bounding boxes
#         for i in range(len(boxes)):
#             # extract the bounding box coordinates
#             xmin, ymin, xmax, ymax = (
#                 int(boxes[i][0]),
#                 int(boxes[i][1]),
#                 int(boxes[i][2]),
#                 int(boxes[i][3]),
#             )
#             # append the bounding box of the number plate
#             number_plate_list.append([[xmin, ymin, xmax, ymax], confidences[i]])

#             # draw the bounding box and the label on the image
#             cv2.rectangle(image, (xmin, ymin), (xmax, ymax), COLOR, 3)
#             text = "Number Plate: {:.2f}%".format(confidences[i] * 100)
#             cv2.putText(
#                 image, text, (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2
#             )

#             if display:
#                 # crop the detected number plate region
#                 number_plate = image[ymin:ymax, xmin:xmax]
#                 # display the number plate
#                 cv2.imshow(f"Number plate {i}", number_plate)

#         end = time.time()
#         # show the time it took to detect the number plates
#         print(
#             f"Time to detect the number plates: {(end - start) * 1000:.0f} milliseconds"
#         )
#         # return the list containing the bounding
#         # boxes of the number plates
#         return number_plate_list
#     # if there are no detections, show a custom message
#     else:
#         print("No number plates have been detected.")
#         return []


# def recognize_number_plates(
#     image_or_path, reader, number_plate_list, write_to_csv=False
# ):

#     start = time.time()
#     # if the image is a path, load the image; otherwise, use the image
#     image = (
#         cv2.imread(image_or_path) if isinstance(image_or_path, str) else image_or_path
#     )

#     for i, box in enumerate(number_plate_list):
#         # crop the number plate region
#         np_image = image[box[0][1] : box[0][3], box[0][0] : box[0][2]]

#         # detect the text from the license plate using the EasyOCR reader
#         detection = reader.readtext(np_image, paragraph=True)

#         if len(detection) == 0:
#             # if no text is detected, set the `text` variable to an empty string
#             text = ""
#         else:
#             # set the `text` variable to the detected text
#             text = str(detection[0][1])

#         # update the `number_plate_list` list, adding the detected text
#         number_plate_list[i].append(text)

#     if write_to_csv:
#         # open the CSV file
#         csv_file = open("number_plates.csv", "w")
#         # create a writer object
#         csv_writer = csv.writer(csv_file)
#         # write the header
#         csv_writer.writerow(["image_path", "box", "text"])

#         # loop over the `number_plate_list` list
#         for box, text in number_plate_list:
#             # write the image path, bounding box coordinates,
#             # and detected text to the CSV file
#             csv_writer.writerow([image_or_path, box, text])
#         # close the CSV file
#         csv_file.close()

#     end = time.time()
#     # show the time it took to recognize the number plates
#     print(
#         f"Time to recognize the number plates: {(end - start) * 1000:.0f} milliseconds"
#     )

#     return number_plate_list


# # if this script is executed directly, run the following code
# if __name__ == "__main__":

#     # load the model from the local directory
#     model = YOLO("model/best.pt")
#     # initialize the EasyOCR reader
#     reader = Reader(["en"], gpu=True)

#     # path to an image or a video file
#     file_path = "datasets/images/test/0fc216ca-131.jpg"
#     # Extract the file name and the file extension from the file path
#     _, file_extension = os.path.splitext(file_path)

#     # Check the file extension
#     if file_extension in [".jpg", ".jpeg", ".png"]:
#         print("Processing the image...")

#         image = cv2.imread(file_path)
#         number_plate_list = detect_number_plates(image, model)
#         cv2.imshow("Image", image)
#         cv2.waitKey(0)

#         # if there are any number plates detected, recognize them
#         if number_plate_list != []:
#             number_plate_list = recognize_number_plates(
#                 file_path, reader, number_plate_list, write_to_csv=True
#             )

#             for box, text in number_plate_list:
#                 cv2.putText(
#                     image,
#                     text,
#                     (box[0], box[3] + 15),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     COLOR,
#                     2,
#                 )
#             cv2.imshow("Image", image)
#             cv2.waitKey(0)

#     elif file_extension in [".mp4", ".mkv", ".avi", ".wmv", ".mov"]:
#         print("Processing the video...")

#         video_cap = cv2.VideoCapture(file_path)

#         # grab the width and the height of the video stream
#         frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#         frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#         fps = int(video_cap.get(cv2.CAP_PROP_FPS))
#         # initialize the FourCC and a video writer object
#         fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#         writer = cv2.VideoWriter("output.mp4", fourcc, fps, (frame_width, frame_height))

#         # loop over the frames
#         while True:
#             # starter time to computer the fps
#             start = time.time()
#             success, frame = video_cap.read()

#             # if there is no more frame to show, break the loop
#             if not success:
#                 print("There are no more frames to process." " Exiting the script...")
#                 break

#             number_plate_list = detect_number_plates(frame, model)

#             if number_plate_list != []:
#                 number_plate_list = recognize_number_plates(
#                     frame, reader, number_plate_list
#                 )

#                 for box, text in number_plate_list:
#                     cv2.putText(
#                         frame,
#                         text,
#                         (box[0], box[3] + 15),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         0.75,
#                         COLOR,
#                         2,
#                     )

#             # end time to compute the fps
#             end = time.time()
#             # calculate the frame per second and draw it on the frame
#             fps = f"FPS: {1 / (end - start):.2f}"
#             cv2.putText(
#                 frame, fps, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8
#             )

#             # show the output frame
#             cv2.imshow("Output", frame)
#             # write the frame to disk
#             writer.write(frame)
#             # if the 'q' key is pressed, break the loop
#             if cv2.waitKey(10) == ord("q"):
#                 break

#         # release the video capture, video writer, and close all windows
#         video_cap.release()
#         writer.release()
#         cv2.destroyAllWindows()
