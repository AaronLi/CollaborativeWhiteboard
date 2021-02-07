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

testImg = cv2.imread("E:\\MISC\\Photos\\1506643681.jpg")

drawboard = np.zeros((480,640,3))

Tool = OnHand(drawboard)

detector = apriltag.Detector(families='tag36h11',
                             nthreads=1,
                             quad_decimate=1.0,
                             quad_sigma=0.0,
                             refine_edges=1,
                             decode_sharpening=0.25)

warp = SurfaceDetection
cv2.namedWindow("DrawWindow")


while 1:
    ret,frame = cam.read()

    cv2.setMouseCallback('DrawWindow', Tool.Draw)

    if ret:

        fixed_frame = warp.display(frame,drawboard, DanCam, detector, (640,480))

        if fixed_frame is not None:
            cv2.imshow("fixed_frame",fixed_frame)
            print("Fixed framu")

        else:
            frame = cv2.undistort(frame, DanCam.mtx, DanCam.dist, None, None)
            for center in centers:
                cv2.circle(frame,tuple(int(i) for i in center),5,(0,0,255),-1)


            cv2.imshow("fixed_frame",frame)
            print("Doo doo frame")

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
            Tool.set_mode(Write)
        elif k == 69 or k == 101:
            Tool.set_mode(Erase)