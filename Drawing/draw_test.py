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


img = np.zeros((720,1280,3), np.float32)
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