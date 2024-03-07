"""
Zeyu Li
Fall 2023, CS5001
Final project
This Marble class is provided by Professor K, and I did some mordifications
to better matches my needs.
"""

import turtle

MARBLE_RADIUS = 15

class Marble:
    """
    Most Marble class is untouched.
    I changed Point to direct use x and y to record the position.
    I added an extra attribute called deactivate to track whether a marble is clicked.
    I deleted some attributes that are not used.
    """
    def __init__(self, x, y, color = "black", size = MARBLE_RADIUS, fill = True, deactivate = False):
        self.pen = self.new_pen()
        self.pen.color(color)
        self.color = color
        self.deactivate = deactivate
        self.x = x
        self.y = y
        self.pen.hideturtle()
        self.size = size
        self.fill = fill
        self.pen.speed(0)  # set to fastest drawing

    def new_pen(self): 
        return turtle.Turtle()

    def set_color(self, color):
        self.color = color
        self.pen.color(self.color)

    def get_color(self):
        return self.color

    def draw(self):
        self.pen.up()
        self.pen.goto(self.x, self.y)
        self.pen.down()
        if self.fill:
            self.pen.fillcolor(self.color)
            self.pen.begin_fill()
            self.pen.circle(self.size)
            self.pen.end_fill()
        else:
            self.pen.color("black")
            self.pen.circle(self.size)

    def draw_empty(self):
        self.erase()
        self.pen.up()
        self.pen.goto(self.x, self.y)
        self.pen.down()
        self.pen.color("black")
        self.pen.circle(self.size)
        
    def erase(self):
        self.pen.clear()

    def clicked_in_region(self, x, y):
        if abs(x - self.x) <= self.size and \
           (y - self.y) <= self.size * 2 and (y - self.y >= 0):
            return True
        return False
    
    def goto(self, x, y):
        self.x = x
        self.y = y
