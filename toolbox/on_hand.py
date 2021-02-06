from toolbox.color import Color
from toolbox.draw import Write

import cv2


class OnHand:
    def __init__(self):
        self.current_tool = None
        self.size = 6
        self.color = Color.RED
        self.color_index = 0
        self.isdown = False

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

    def Draw(self, img, event, x, y):

        if event==cv2.EVENT_LBUTTONDOWN:
            self.isdown = True
        elif event==cv2.EVENT_LBUTTONUP:
            self.isdown = False

        if self.current_tool is not None and self.isdown:
            self.current_tool.draw(img, event, x, y, self.size, self.color)

    def next_color(self):
        self.color_index = (self.color_index+1)%len(Color.COLOR_LIST)
        self.color = Color.COLOR_LIST[self.color_index]
