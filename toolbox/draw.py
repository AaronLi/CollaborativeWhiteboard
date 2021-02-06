import cv2
from on_hand import OnHand
from drawing_mode import DrawingMode

class Write:
    def __init__(self):
        #self.size = 1
        #self.color = (0,0,255)


    def draw(self,img,event,x,y,size,color):
        if event == cv2.EVENT_LBUTTONDOWN:
            #drawmode = DrawingMode.DRAWING
            cv2.circle(img, (x, y), size, color, -1)

        elif event == cv2.EVENT_MOUSEMOVE:
            #if drawmode == DrawingMode.DRAWING:
            cv2.circle(img, (x, y), size, color, -1)

        elif event == cv2.EVENT_LBUTTONUP:
            OnHand.set_mode(None)
