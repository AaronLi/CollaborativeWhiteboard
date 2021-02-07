import cv2

class Erase:
    def __init__(self):
        self.prev_coord = (0,0)

    def DrawStart(self,img, x, y, size, color):
        cv2.circle(img, (x, y), size//2, (0,0,0), -1)
        self.prev_coord = (x,y)

    def DrawMove(self,img, x, y, size, color):
        cv2.line(img, (x, y), self.prev_coord, (0, 0, 0), size)
        self.prev_coord = (x, y)

    #def DrawStop(self,img, x, y, size, color):