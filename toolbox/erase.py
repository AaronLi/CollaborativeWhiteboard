import cv2
from drawing_mode import DrawingMode

class Erase:
    def __init__(self):
        #self.size = 20
        #self.color = (0, 0, 0)
        #self.drawmode = None

    #def sizeUp(self):
        #self.size+=5

    #def sizeDown(self):
        #self.size-=5

    def Draw(self,img,event,x,y,size,color):

        if event == cv2.EVENT_LBUTTONDOWN:
            #self.drawmode = DrawingMode.DRAWING
            cv2.circle(img, (x, y), self.size, (0,0,0), -1)

        elif event == cv2.EVENT_MOUSEMOVE:
            #if self.drawmode == DrawingMode.DRAWING:
            cv2.circle(img, (x, y), self.size, (0,0,0), -1)
