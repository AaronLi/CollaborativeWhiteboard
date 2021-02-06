import cv2
import numpy as np

img = np.zeros((1080,1920,3), np.uint8)
while(1):
    cv2.imshow('img',img)
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its

# appears to just use ASCII values for most inputs