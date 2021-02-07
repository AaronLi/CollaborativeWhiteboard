import cv2
import numpy as np
import pupil_apriltags as apriltag
from Drawing.toolbox.on_hand import OnHand
from Drawing.toolbox.erase import Erase
from Drawing.toolbox.draw import Write
from surface_detect.warp_surface import SurfaceDetection, detector
from surface_detect.cam_config import *
from sync_board import SyncableBoard
height = 480
width = 640

cam = cv2.VideoCapture(1)
cam.set(3, width)
cam.set(4, height)

sync_board = SyncableBoard("http://34.122.107.117:5000")
sync_board.set_array(np.zeros((height,width,3), dtype=np.uint8))
sync_board.start_syncing()

Tool = OnHand(sync_board.array)

presentation_images = cv2.imread("E:\\MISC\\MacHacks\\WhiteoardPython\\presentation\\photo_3")

warp = SurfaceDetection
cv2.namedWindow("DrawWindow")
cv2.setMouseCallback('DrawWindow', Tool.mouse)
pen = Write()
eraser = Erase()

while 1:
    ret,frame = cam.read()
    drew_drawing = False
    if ret:
        #frame = cv2.rotate(frame,cv2.ROTATE_180)
        fixed_frame, _ = warp.display(frame, sync_board.array, PSEyeCam, detector,(width,height)) # frame,drawboard, DanCam, detector,(640,480)
        #final_display = np.hstack(fixed_frame,drawboard)
        if fixed_frame is not None:
            cv2.imshow("fixed_frame",fixed_frame)
            focused_frame, _ = warp.undistort(fixed_frame, PSEyeCam, detector, (width,height), _)
            if focused_frame is not None:
                cv2.imshow('DrawWindow', focused_frame)
                drew_drawing = True
        else:
            frame = cv2.undistort(frame, PSEyeCam.mtx, PSEyeCam.dist, None, None)
            #for center in centers:
            #    cv2.circle(frame,tuple(int(i) for i in center),5,(0,0,255),-1)


            cv2.imshow("fixed_frame",frame)
        if not drew_drawing:
            cv2.imshow('DrawWindow', sync_board.array)
    k = cv2.waitKey(1) & 0xFF

    if k == 27:
        break
    elif k == 43 or k == 61:
        Tool.sizeUp()
    elif k == 45:
        Tool.sizeDown()
    elif k == 99 or k == 67:
        Tool.next_color()
    elif k == 68 or k == 100:
        Tool.set_mode(pen)
    elif k == 69 or k == 101:
        Tool.set_mode(eraser)