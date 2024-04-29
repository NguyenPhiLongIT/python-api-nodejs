import flask
import cv2
import sys
import os
import time 

def read_images_from_directory(directory_path):
    images = []
    # Lặp qua tất cả các file trong thư mục
    for filename in os.listdir(directory_path):
        # Kiểm tra nếu file có phần mở rộng hợp lệ (ví dụ: .jpg, .png)
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Đọc ảnh từ đường dẫn của file
            image_path = os.path.join(directory_path, filename)
            image = cv2.imread(image_path)
            if image is not None:
                print("Đã đọc ảnh từ:", image_path)
                images.append(image)
            else:
                print("Không thể đọc ảnh từ:", image_path)
    return images
new_frame_time = time.time()
# for (top, right, bottom, left), name in zip(face_locations, face_names):
#     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#     # top *= 2
#     # right *= 2
#     # bottom *= 2
#     # left *= 2

#     # Draw a box around the face
#     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#     # Draw a label with a name below the face
#     cv2.rectangle(
#         frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
#     )
#     font = cv2.FONT_HERSHEY_DUPLEX
#     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



# Display the resulting image
# cv2.imshow("Video", frame)
# curr_time = time.localtime()
# curr_clock = time.strftime("%c", curr_time)
# #print(curr_clock)
# cv2.destroyAllWindows()