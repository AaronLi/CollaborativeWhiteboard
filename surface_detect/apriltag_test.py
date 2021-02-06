import numpy
import numpy as np
import cv2
from pupil_apriltags import Detector
#import mathutils
#from google.colab.patches import cv2_imshow

numpy.set_printoptions(linewidth=500)

fx = 1070.1204833984375
fy = 1081.240966796875
cx = 930.6589242069822
cy = 653.0827256735793
camera_intrinsics_vector = [fx, fy, cx, cy]

def rot_matrix_to_euler(R):
    y_rot = numpy.arcsin(R[2][0])
    x_rot = numpy.arccos(R[2][2]/numpy.cos(y_rot))
    z_rot = numpy.arccos(R[0][0]/numpy.cos(y_rot))
    y_rot_angle = y_rot *(180/numpy.pi)
    x_rot_angle = x_rot *(180/numpy.pi)
    z_rot_angle = z_rot *(180/numpy.pi)
    return (x_rot_angle,y_rot_angle,z_rot_angle)

image = cv2.imread("E:\\MISC\\MacHacks\\WhiteoardPython\\surface_detect\\apriltag_photos\\april3.jpg")

bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

detector = Detector(families='tag36h11',
                             nthreads=1,
                             quad_decimate=1.0,
                             quad_sigma=0.0,
                             refine_edges=1,
                             decode_sharpening=0.25,
                             debug=0)
detections = detector.detect(bw_image, estimate_tag_pose=True, camera_params=(fx, fy, cx, cy), tag_size=0.074)

for detection in detections:

    center = detection.center.astype(numpy.int32)
    cv2.circle(image, (center[0], center[1]), 3, (0, 255, 0), -1)

    corners = detection.corners.astype(numpy.int32)
    cv2.polylines(image, [corners], True, (0, 255, 0), thickness = 2)

    orientation = numpy.array([50, 0, 0])
    orientation = numpy.transpose(orientation)
    # endpoint = numpy.matmul(detection.pose_R, orientation).astype(numpy.int32) * 20
    orientation_line = numpy.matmul(detection.pose_R, orientation)

    euler_angles = rot_matrix_to_euler(detection.pose_R)

    # endpoint = numpy.array( [center[0] + int(orientation_line[0]), center[1] - int(orientation_line[1]) ] )
    endpoint = numpy.array( [center[0] + int(numpy.cos(euler_angles[0]) * 100), center[1] - int(numpy.sin(euler_angles[0]) * 100) ] )

    cv2.line(image, (center[0], center[1]), (endpoint[0], endpoint[1]), (0, 0, 255), 2)
    # cv2.line(image, (center[0], center[1]), (center[0] + endpoint[0], center[1] + endpoint[1]), (0, 0, 255), 2)

    # print(detection.pose_R.shape)
    # print(detection.pose_t)
    # print(orientation.shape)
    # print( numpy.matmul(detection.pose_R, orientation)  )

    # print(rot_matrix_to_euler(detection.pose_R))

cv2.imshow("Image", image)
cv2.waitKey(0)