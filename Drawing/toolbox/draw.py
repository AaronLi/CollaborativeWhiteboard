import cv2


class Write:
    def __init__(self):
        self.prev_coord = (0,0)

    def DrawStart(self,img, x, y, size, color):
        cv2.circle(img, (x, y), size//2, color, -1)
        self.prev_coord = (x,y)

    def DrawMove(self,img, x, y, size, color):
        cv2.line(img, (x, y), self.prev_coord, color, size)
        self.prev_coord = (x, y)

    #def DrawStop(self,img, x, y, size, color):
