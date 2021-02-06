import pupil_apriltags as apriltag
import cv2
import numpy as np
import argparse

fx = 1070.1204833984375
fy = 1081.240966796875
cx = 930.6589242069822
cy = 653.0827256735793

cameraMatrix = np.array([[fx, 0, cx],
                [0, fy, cy],
                [0, 0, 1]])



def draw_pose(overlay, camera_params, tag_size, tag, z_sign=1):
    opoints = np.array([
        -2, -2, 0,
        2, -2, 0,
        2, 2, 0,
        2, -2, -4 * z_sign,
    ]).reshape(-1, 1, 3) * 0.5 * tag_size

    # fx, fy, cx, cy = camera_params
    fx = 1070.1204833984375
    fy = 1081.240966796875
    cx = 930.6589242069822
    cy = 653.0827256735793

    K = np.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape(3, 3)

    rvec, _ = cv2.Rodrigues(r.pose_R[:3, :3])
    tvec = r.pose_R[:3, 2]

    dcoeffs = np.zeros(5)

    ipoints, _ = cv2.projectPoints(opoints, rvec, tvec, K, dcoeffs)

    ipoints = np.round(ipoints).astype(int)

    ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

    cv2.line(overlay, tag.center[0], tag.center[1], (0, 0, 255), 2)
    cv2.line(overlay, ipoints[1], ipoints[2], (0, 255, 0), 2)
    cv2.line(overlay, ipoints[1], ipoints[3], (255, 0, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(overlay, 'X', ipoints[0], font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(overlay, 'Y', ipoints[2], font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(overlay, 'Z', ipoints[3], font, 0.5, (255, 0, 0), 2, cv2.LINE_AA)


def _draw_cube(self, overlay, camera_params, tag_size, pose, centroid, z_sign=1):
    opoints = np.array([
        -10, -8, 0,
        10, -8, 0,
        10, 8, 0,
        -10, 8, 0,
        -10, -8, 2 * z_sign,
        10, -8, 2 * z_sign,
        10, 8, 2 * z_sign,
        -10, 8, 2 * z_sign,
    ]).reshape(-1, 1, 3) * 0.5 * tag_size

    edges = np.array([
        0, 1,
        1, 2,
        2, 3,
        3, 0,
        0, 4,
        1, 5,
        2, 6,
        3, 7,
        4, 5,
        5, 6,
        6, 7,
        7, 4
    ]).reshape(-1, 2)

    # fx, fy, cx, cy = camera_params
    fx = 1070.1204833984375
    fy = 1081.240966796875
    cx = 930.6589242069822
    cy = 653.0827256735793

    K = np.array([fx, 0, cx, 0, fy, cy, 0, 0, 1]).reshape(3, 3)

    rvec, _ = cv2.Rodrigues(pose[:3, :3])
    tvec = pose[:3, 3]

    dcoeffs = np.zeros(5)

    ipoints, _ = cv2.projectPoints(opoints, rvec, tvec, K, dcoeffs)

    ipoints = np.round(ipoints).astype(int)

    ipoints = [tuple(pt) for pt in ipoints.reshape(-1, 2)]

    for i, j in edges:
        cv2.line(overlay, ipoints[i], ipoints[j], (0, 255, 0), 1, 16)


print("[INFO] loading image...")
image = cv2.imread("E:\\MISC\\MacHacks\\WhiteoardPython\\surface_detect\\apriltag_photos\\april2.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# define the AprilTags detector options and then detect the AprilTags
# in the input image
print("[INFO] detecting AprilTags...")
detector = apriltag.Detector(families='tag36h11',
                             nthreads=1,
                             quad_decimate=1.0,
                             quad_sigma=0.0,
                             refine_edges=1,
                             decode_sharpening=0.25,
                             debug=0)
# options = apriltag.Detectoroptions(families="tag36h11",border=1,
#                                  nthreads=4,
#                                  quad_decimate=1.0,
#                                  quad_blur=0.0,
#                                  refine_edges=True,
#                                  refine_decode=False,
#                                  refine_pose=False,
#                                  debug=False,
#                                  quad_contours=True)

tagSize = 0.074

results = detector.detect(gray, estimate_tag_pose=True, camera_params=(fx, fy, cx, cy), tag_size=tagSize)
print("[INFO] {} total AprilTags detected".format(len(results)))

for r in results:
    # extract the bounding box (x, y)-coordinates for the AprilTag
    # and convert each of the (x, y)-coordinate pairs to integers
    (ptA, ptB, ptC, ptD) = r.corners
    ptB = (int(ptB[0]), int(ptB[1]))
    ptC = (int(ptC[0]), int(ptC[1]))
    ptD = (int(ptD[0]), int(ptD[1]))
    ptA = (int(ptA[0]), int(ptA[1]))
    # draw the bounding box of the AprilTag detection
    cv2.line(image, ptA, ptB, (0, 255, 0), 2)
    cv2.line(image, ptB, ptC, (0, 255, 0), 2)
    cv2.line(image, ptC, ptD, (0, 255, 0), 2)
    cv2.line(image, ptD, ptA, (0, 255, 0), 2)
    # draw the center (x, y)-coordinates of the AprilTag
    (cX, cY) = (int(r.center[0]), int(r.center[1]))
    cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
    # draw the tag family on the image
    tagFamily = r.tag_family.decode("utf-8")
    pose_rotation = str(np.round(r.pose_R, 2))
    pose_translation = str(np.round(r.pose_t, 2))

    rvec = cv2.Rodrigues(r.pose_R)[0]
    z_vec = np.array([0, 0, 1], dtype=float)



    p_out,_ = cv2.projectPoints(z_vec, rvec ,np.zeros(3,dtype=float), cameraMatrix,np.zeros(5,dtype=float)) #v(r.center[0], r.center[1])
    p_out = p_out[0,0]
    print(r.center)
    print(p_out)
    cv2.line(image, tuple(int(i) for i in r.center), tuple(int(i) for i in p_out), (0, 255, 0), 2)

    #cv2.line(image, (r.center[0], r.center[1]), ptB, (0, 255, 0), 2)
    cv2.putText(image, tagFamily , (ptA[0], ptA[1] - 50),
                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # cv2.putText(image, pose_rotation, (ptA[0], ptA[1] - 30),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # cv2.putText(image, pose_translation, (ptA[0], ptA[1] - 10),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    print("[INFO] tag family: {}".format(tagFamily))

# show the output image after AprilTag detection
cv2.imshow("Image", image)
cv2.waitKey(0)
