import cv2
import numpy as np
r_slider_max = 255
title_window = 'colour thresholding'
lab_colour_range = np.array(
    (((116, 124, 132),(255, 157, 255)),), dtype=np.uint8
)

cam = cv2.VideoCapture(1)

def on_r_trackbar(val):
    lab_colour_range[0][0][0] = int(val)
def on_g_trackbar(val):
    lab_colour_range[0][0][1] = int(val)
def on_b_trackbar(val):
    lab_colour_range[0][0][2] = int(val)

def on_rm_trackbar(val):
    lab_colour_range[0][1][0] = int(val)
def on_gm_trackbar(val):
    lab_colour_range[0][1][1] = int(val)
def on_bm_trackbar(val):
    lab_colour_range[0][1][2] = int(val)

running = True
cv2.namedWindow(title_window)
trackbar_name = 'Alpha x %d' % r_slider_max
cv2.createTrackbar("lmin", title_window, lab_colour_range[0][0][0], 255, on_r_trackbar)
cv2.createTrackbar("amin", title_window, lab_colour_range[0][0][1], 255, on_g_trackbar)
cv2.createTrackbar("bmin", title_window, lab_colour_range[0][0][2], 255, on_b_trackbar)
cv2.createTrackbar("lmax", title_window, lab_colour_range[0][1][0], 255, on_rm_trackbar)
cv2.createTrackbar("amax", title_window, lab_colour_range[0][1][1], 255, on_gm_trackbar)
cv2.createTrackbar("bmax", title_window, lab_colour_range[0][1][2], 255, on_bm_trackbar)
# Show some stuff
while running:
    ret, frame = cam.read()
    if ret:
        frame = cv2.blur(frame, (7, 7))
        lab_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        thresh_frame = cv2.inRange(lab_frame, lab_colour_range[0][0], lab_colour_range[0][1])
        bgr_lab_frame = cv2.cvtColor(lab_frame, cv2.COLOR_LAB2BGR)
        bgr_thresh_frame = cv2.cvtColor(thresh_frame, cv2.COLOR_GRAY2BGR)
        collage = np.hstack((bgr_lab_frame, bgr_thresh_frame))
        cv2.imshow(title_window, collage)
    if cv2.waitKey(1) == 27:
        running = False

cam.release()
cv2.destroyAllWindows()
print(lab_colour_range)