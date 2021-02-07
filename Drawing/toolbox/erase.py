import cv2

class Erase:
    def __init__(self):
        self.prev_coord(0,0)

    @staticmethod
    def draw(self,img,event,x,y,size,color):

        if event == cv2.EVENT_LBUTTONDOWN:
            #self.drawmode = DrawingMode.DRAWING
            cv2.circle(img, (x, y), size, (0,0,0), -1)
            self.prev_coord = (x,y)

        elif event == cv2.EVENT_MOUSEMOVE:
            #if self.drawmode == DrawingMode.DRAWING:
            cv2.circle(img, (x, y), size, (0,0,0), -1)
            cv2.line(img, (x, y), self.prev_coord, (0,0,0), size)
            self.prev_coord=(x,y)