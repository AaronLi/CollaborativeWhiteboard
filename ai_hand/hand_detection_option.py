"""
Real time 2D and 3D hand pose estimation using RGB webcam
"""
import cv2

from Drawing.toolbox.draw import Write
from Drawing.toolbox.erase import Erase
from Drawing.toolbox.on_hand import OnHand
from surface_detect.cam_config import *
from surface_detect.warp_surface import SurfaceDetection, detector
import numpy as np
from sync_board import SyncableBoard

#hand_pose_detector = HandPoseDetector()
# webcam settings - default image size [640x480]
height = 1080
width = 1920
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

hand_detector = cv2.CascadeClassifier("cascade.xml")

surface_detector = SurfaceDetection()

SKIN_BOUNDS = np.array(
    (((116, 124, 132), (255, 157, 255)),), dtype=np.uint8
)

drawboard = np.zeros((height,width,3), dtype=np.uint8)

Tool = OnHand(drawboard)
drawboard = SyncableBoard("http://localhost:5000")
drawboard.set_array(np.zeros((480,640,3), dtype=np.uint8))
drawboard.start_syncing()
print(drawboard.sync_runner.is_alive())
Tool = OnHand(drawboard.array)

warp = SurfaceDetection
pen = Write()
eraser = Erase()
penX, penY = None, None
Tool.set_mode(pen)
had_box = False
alpha = 0.7
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    fixed_frame, _ = warp.display(frame.copy(), drawboard, DanCam, detector,(width,height))
    if fixed_frame is not None:
        undistorted_frame, _ = surface_detector.undistort(frame, DanCam, detector, (width, height), _,fix_distorsion=True)
        if undistorted_frame is not None:
            frame = undistorted_frame

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #est_pose_uv, est_pose_cam_xyz = hand_pose_detector.detect(frame)
            boxes = hand_detector.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=10,minSize=(100,100))
            has_box = False
            for x, y, w, h in boxes:
                print(w, h)

                #y = 480-y
                box_center_x, box_center_y = x+w//2, y+h//2
                if penX is None and penY is None:
                    penX = box_center_x
                    penY = box_center_y
                else:
                    penX = penX * alpha + box_center_x * (1-alpha)
                    penY = penY * alpha + box_center_y * (1-alpha)
                cv2.rectangle(undistorted_frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                has_box = True
            if penX is not None and penY is not None:
                if has_box:
                    cv2.circle(undistorted_frame, (int(penX), int(penY)), 5, (0, 0, 255), thickness=-1)
                    if not had_box:
                        Tool.DrawStart(int(penX), int(penY), None, None)
                    Tool.DrawMove(int(penX), int(penY), None, None)
                else:
                    Tool.DrawStop()
                    penX = None
                    penY = None
            had_box = has_box
        # draw 2D hand pose
        #skeleton_frame = draw_2d_skeleton(original_frame, est_pose_uv)

        cv2.imshow("preview", np.hstack((fixed_frame, undistorted_frame)))

    else:
        cv2.imshow("preview", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # print frame per second
    # fps = cap.get(cv2.CV_CAP_PROP_FPS)
    # print(fps," fps")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
