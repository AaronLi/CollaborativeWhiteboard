import cv2
import numpy as np
from Drawing.toolbox.on_hand import OnHand
from Drawing.toolbox.erase import Erase
from Drawing.toolbox.draw import Write

Tool = OnHand()
# mouse callback function
def interactive_drawing(event,x,y,size,flag):
    #global ix,iy,drawmode, mode,erasing

    Tool.Draw(img,event,x,y)


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


img = np.zeros((720,1280,3), np.uint8)
cv2.namedWindow('Window')
cv2.setMouseCallback('Window',interactive_drawing)
while(1):
    cv2.imshow('Window',img)
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break
    elif k==43 or k==61:
        Tool.sizeUp()
    elif k==45:
        Tool.sizeDown()
    elif k==99 or k==67:
        Tool.next_color()
    elif k==68 or k==100:
        Tool.set_mode(Write)
    elif k==69 or k==101:
        Tool.set_mode(Erase)

cv2.destroyAllWindows()