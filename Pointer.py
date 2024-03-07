"""
Zeyu Li
Fall2023, CS5001
Final project
This file contains Pointer class
"""

import turtle

class Pointer:
    """
    This is the top left pointer on GUI.
    """
    def __init__(self, x, y, pic = "pointer.gif") -> None:
        self.x = x
        self.y = y
        self.screen = turtle.Screen()
        self.screen.addshape(pic)
        self.pen = turtle.Turtle()
        self.pen.shape(pic)
        self.pen.up()
        self.pen.goto(x,y)
    
    
    def next(self, distance):
        """
        Move the pointer up or down for a fixed distance.
        """
        self.y = self.y - distance
        self.pen.goto(self.x, self.y)