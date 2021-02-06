import cv2
import numpy as np
from toolbox.on_hand import OnHand
from drawing_mode import DrawingMode
from toolbox.erase import Erase
from toolbox.draw import Write


drawmode = DrawingMode.DRAWING

# mouse callback function
def interactive_drawing(event,x,y,size,flags):
    global ix,iy,drawmode, mode,erasing

    OnHand.draw(img,event,x,y)


    # drawing
    #    cv2.circle(img, (x, y), 1, (0, 0, 255), -1)

    #elif event==cv2.EVENT_MOUSEMOVE:
    #    if drawmode==DrawingMode.DRAWING:
    #            cv2.circle(img,(x,y),1,(0,0,255),-1)

    #elif event==cv2.EVENT_LBUTTONUP:
    #    drawmode = DrawingMode.NONE


    # erasing

    #if event==cv2.EVENT_RBUTTONDOWN:
    #    drawmode=DrawingMode.ERASING
    #    cv2.circle(img, (x, y), 25, (0, 0, 0), -1)

    #elif event==cv2.EVENT_MOUSEMOVE:
    #    if drawmode==DrawingMode.ERASING:
    #        # check for cv2.circle at that point and delete it
    #        # for now just put a black circle in its place
    #        cv2.circle(img, (x, y), 25, (0, 0, 0), -1)

    #elif event==cv2.EVENT_RBUTTONUP:
    #    drawmode=DrawingMode.NONE

    # change pen size


img = np.zeros((1080,1920,3), np.uint8)
cv2.namedWindow('Window')
cv2.setMouseCallback('Window',interactive_drawing)
while(1):
    cv2.imshow('Window',img)
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break
    elif k==43:
        OnHand.sizeUp()
    elif k==45:
        OnHand.sizeDown()
    elif k==99 or 67:
        OnHand.next_color()
    elif k==68 or 100:
        OnHand.set_mode(Write)
    elif k==69 or 101:
        OnHand.set_mode(Erase)

cv2.destroyAllWindows()