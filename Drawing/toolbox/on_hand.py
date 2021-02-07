from Drawing.toolbox.color import Color

import cv2


class OnHand:
    def __init__(self,image):
        self.current_tool = None
        self.size = 6
        self.color = Color.RED
        self.color_index = 0
        self.isdown = False
        self.img = image

    def set_mode(self, drawmode):
        self.current_tool = drawmode
        print("Tool selected:",drawmode)

    def sizeUp(self):
        self.size += 5
        print("Current size",self.size)

    def sizeDown(self):
        if self.size>5:
            self.size -= 5
        print("Current size",self.size)

    def DrawStart(self, x, y, flags, param):
        self.isdown = True
        self.current_tool.DrawStart(self.img, x, y, self.size, self.color)

    def DrawMove(self, x, y, flags, param):
        if self.isdown:
            self.current_tool.DrawMove(self.img, x, y, self.size, self.color)

    def DrawStop(self, x, y, flags, param):
        self.isdown = False


    def next_color(self):
        self.color_index = (self.color_index+1)%len(Color.COLOR_LIST)
        self.color = Color.COLOR_LIST[self.color_index]
