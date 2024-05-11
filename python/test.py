from ultralytics import YOLO
import cv2
from train import detect_number_plates

# from easyocr import Reader
import os

# Đường dẫn tới tệp hình ảnh
img_path = "image/y.jpg"

# Kiểm tra xem tệp hình ảnh có tồn tại không
try:
    with open(img_path, "rb") as f:
        pass
except FileNotFoundError:
    print(f"File {img_path} does not exist.")
    exit()

# Khởi tạo mô hình YOLO
# model = YOLO(".train/best.pt")

# # Thực hiện dự đoán trên hình ảnh
# results = model.predict(img_path, save=True)  # working

# print("hello")
if __name__ == "__main__":

    # load the model from the local directory
    model = YOLO(".train/best.pt")
    # # initialize the EasyOCR reader
    # reader = Reader(["en"], gpu=True)

    # path to an image or a video file
    path = "./public/uploads/result/"
    file_path = path + "r.jpg"
    # Extract the file name and the file extension from the file path
    _, file_extension = os.path.splitext(file_path)

    # Check the file extension
    if file_extension in [".jpg", ".jpeg", ".png"]:
        print("Processing the image...")

        image = cv2.imread(file_path)
        number_plate_list = detect_number_plates(image, model)
        cv2.imwrite(path + "output_image3.jpg", image)
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)

        # if there are any number plates detected, recognize them
        # if number_plate_list != []:
        #     number_plate_list = recognize_number_plates(
        #         file_path, reader, number_plate_list, write_to_csv=True
        #     )

        #     for box, text in number_plate_list:
        #         cv2.putText(
        #             image,
        #             text,
        #             (box[0], box[3] + 15),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             0.5,
        #             COLOR,
        #             2,
        #         )
        #     cv2.imshow("Image", image)
        #     cv2.waitKey(0)
