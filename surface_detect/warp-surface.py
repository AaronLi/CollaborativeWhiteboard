import cv2
import numpy as np
import pupil_apriltags as apriltag
from surface_detect.cam_config import DanCam
# would already have the centers from april

detector = apriltag.Detector(families='tag36h11',
                                 nthreads=1,
                                 quad_decimate=1.0,
                                 quad_sigma=0.0,
                                 refine_edges=1,
                                 decode_sharpening=0.25)

def undistort(sourceImage,cam,size):
    width,height = size

    newMtx, validROI = cv2.getOptimalNewCameraMatrix(cam.mtx, cam.dist,(sourceImage.shape[0], sourceImage.shape[1]), 1)

    sourceImage = cv2.undistort(sourceImage, cam.mtx, cam.dist, None, None)

    gray = cv2.cvtColor(sourceImage, cv2.COLOR_BGR2GRAY)

    results = detector.detect(gray, estimate_tag_pose=True,
                              camera_params=(newMtx[0, 0], newMtx[1, 1], newMtx[0, 2], newMtx[1, 2]), tag_size=0.074)
    i = 0

    apriltag_centers = np.zeros((4, 2))

    for r in results:
        apriltag_centers[i] = r.center
        i += 1
    print(i)

    if i<4:
        return None,apriltag_centers


    originalCorners = np.array(apriltag_centers, dtype=np.float32)  # apriltag_centers holds 4 r.center coordinates

    ouputImageWidth = width
    outputImageHeight = height

    # Now put the corners of the output image so the warp knows where to warp to
    destinationCorners = np.array(
        ((0, 0), (ouputImageWidth, 0), (0, outputImageHeight), (ouputImageWidth, outputImageHeight)), dtype=np.float32)


    # Now we have all corners sorted, so we can create the warp matrix
    warpMatrix = cv2.getPerspectiveTransform(originalCorners, destinationCorners, )

    # And now we can warp the Sudoku in the new image
    transformedOutputImage = cv2.warpPerspective(sourceImage, warpMatrix, (ouputImageWidth, outputImageHeight))

    return transformedOutputImage,apriltag_centers

cam = cv2.VideoCapture(0)

while 1:
    ret,frame = cam.read()

    print(frame.shape)

    if ret:

        fixed_frame,centers = undistort(frame,DanCam,(640,480))

        if fixed_frame is not None:
            cv2.imshow("fixed_frame",fixed_frame)
            print("Fixed framu")

        else:
            frame = cv2.undistort(frame, DanCam.mtx, DanCam.dist, None, None)
            for center in centers:
                cv2.circle(frame,tuple(int(i) for i in center),5,(0,0,255),-1)


            cv2.imshow("fixed_frame",frame)
            print("Doo doo frame")

        if cv2.waitKey(1)&0xFF == 27:
            break
