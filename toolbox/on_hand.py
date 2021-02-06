from toolbox.color import Color
from toolbox.draw import Write


import cv2

class OnHand:
    def __init__(self):
        self.current_tool = None
        self.size=6
        self.color=Color.RED
        self.color_index = 0

    def set_mode(self,drawmode):
        self.current_tool=drawmode

    def sizeUp(self):
        self.size+=5

    def sizeDown(self):
        self.size-=5

    def Draw(self,img,event,x,y):
        self.current_tool.draw(img,event,x,y,self.size,self.color)

    def next_color(self):
        self.color_index+=1
        self.color = Color.COLOR_LIST(self.color_index % len(Color.COLOR_LIST))
