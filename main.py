import cv2
import numpy as np
import pupil_apriltags as apriltag
from Drawing.toolbox.on_hand import OnHand
from Drawing.toolbox.erase import Erase
from Drawing.toolbox.draw import Write
from surface_detect.warp_surface import SurfaceDetection
from surface_detect.cam_config import DanCam



#np.hstack for sidebyside










cam = cv2.VideoCapture(0)

#testImg = cv2.imread()

drawboard = np.zeros((480,640,3),dtype=np.uint8)

Tool = OnHand(drawboard)
pen = Write()
eraser = Erase()


detector = apriltag.Detector(families='tag36h11',
                             nthreads=1,
                             quad_decimate=1.0,
                             quad_sigma=0.0,
                             refine_edges=1,
                             decode_sharpening=0.25)

warp = SurfaceDetection
cv2.namedWindow("DrawWindow")
cv2.setMouseCallback('DrawWindow', Tool.mouse)
pen = Write()
eraser = Erase()

while 1:
    ret,frame = cam.read()
    drew_drawing = False
    if ret:
        fixed_frame,_ = warp.display(frame,drawboard, DanCam, detector,(640,480)) # frame,drawboard, DanCam, detector,(640,480)
        #final_display = np.hstack(fixed_frame,drawboard)

        if fixed_frame is not None:
            cv2.imshow("fixed_frame",fixed_frame)
            focused_frame,_ = warp.undistort(fixed_frame, DanCam, detector, (640, 480), _)
            if focused_frame is not None:
                cv2.imshow('DrawWindow', focused_frame)
                drew_drawing = True
        else:
            frame = cv2.undistort(frame, DanCam.mtx, DanCam.dist, None, None)
            #for center in centers:
            #    cv2.circle(frame,tuple(int(i) for i in center),5,(0,0,255),-1)


            cv2.imshow("fixed_frame",frame)
            print("Doo doo frame")
        if not drew_drawing:
            cv2.imshow('DrawWindow', drawboard)
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