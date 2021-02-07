import cv2
import numpy as np
import pupil_apriltags as apriltag
from surface_detect.cam_config import DanCam
# would already have the centers from april

class SurfaceDetection:

    def undistort(self, sourceImage, cam, detector, size):
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

        #return transformedOutputImage,apriltag_centers


    def display(self, sourceImage, frame, cam, detector, size):
        width,height = size

        input_height,input_width,input_depth = frame.shape

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
            return None


        realCorners = np.array(apriltag_centers, dtype=np.float32)  # holds the position of the writing space

        #ouputImageWidth = width
        #outputImageHeight = height

        # corners of the writing
        displayCorners = np.array(
            ((0, 0), (input_width, 0), (0, input_height), (input_width, input_height)), dtype=np.float32)


        # get matrix to warp the writing array to fit the corners of the real space
        warpMatrix = cv2.getPerspectiveTransform(displayCorners, realCorners)

        # use the matrix to warp the image
        transformedOutputImage = cv2.warpPerspective(frame, warpMatrix, (width, height))

        pixels = cv2.inRange(transformedOutputImage,(0,0,0),(0,0,0)) # create a mask with writing

        mask = cv2.bitwise_and(sourceImage,sourceImage,mask=pixels)


        finalFrame = mask+transformedOutputImage # add the camera frame and the writing toghether

        return finalFrame


