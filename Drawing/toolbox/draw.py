import cv2


class Write:
    def __init__(self):
        self.prev_coord = (0,0)

    def draw(self,img,event,x,y,size,color):
        if event == cv2.EVENT_LBUTTONDOWN:
            #drawmode = DrawingMode.DRAWING
            cv2.circle(img, (x, y), size, color, -1)
            self.prev_coord = (x,y)

        elif event == cv2.EVENT_MOUSEMOVE:
            #if drawmode == DrawingMode.DRAWING:
            #cv2.circle(img, (x, y), size, color, -1)
            cv2.line(img, (x, y), self.prev_coord, color, size)
            self.prev_coord = (x, y)
        #elif event == cv2.EVENT_LBUTTONUP:
            #OnHand.set_mode(None)
