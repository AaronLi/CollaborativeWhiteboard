import cv2
import matplotlib.pyplot as plt
import time

cap = cv2.VideoCapture(1)

num_image = 30
last_pic_time = time.time()
captured_frames = 0

while captured_frames < num_image:

    ret, frame = cap.read()

    cv2.imshow("preview", frame)
    if time.time() - last_pic_time > 2:
        print('click!',captured_frames)
        cv2.imwrite(f'camera_parameter_K/calibration_images/img{captured_frames}.png', frame)
        last_pic_time = time.time()
        captured_frames += 1
    if cv2.waitKey(1) == 27:
        break

        
cap.release()
cv2.destroyAllWindows()



























