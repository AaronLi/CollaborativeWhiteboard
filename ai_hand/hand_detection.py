"""
Real time 2D and 3D hand pose estimation using RGB webcam
"""
import cv2
import numpy as np

from ai_hand.hand_pose_detector import HandPoseDetector
from ai_hand.hand_shape_pose.util.vis_pose_only import draw_2d_skeleton

detector = HandPoseDetector()
# webcam settings - default image size [640x480]
cap = cv2.VideoCapture(1)

hand_detector = cv2.CascadeClassifier("cascade.xml")

SKIN_BOUNDS = np.array(
    (((116, 124, 132), (255, 157, 255)),), dtype=np.uint8
)
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = frame[:, 80:560, :]  # cut the frame to 480x480
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    original_frame = frame.copy()

    est_pose_uv, est_pose_cam_xyz = detector.detect(frame)
    boxes = hand_detector.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=10)
    for x, y, w, h in boxes:
        cv2.rectangle(original_frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    # draw 2D hand pose
    skeleton_frame = draw_2d_skeleton(original_frame, est_pose_uv)

    cv2.imshow("preview", skeleton_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # print frame per second
    # fps = cap.get(cv2.CV_CAP_PROP_FPS)
    # print(fps," fps")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
