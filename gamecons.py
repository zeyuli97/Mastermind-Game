"""
Zeyu Li
Fall 2023, CS5001
Final Project
This file contians turtle related game construction.
"""
import random
import Marble as m
import turtle
class GameConstructor:
    """
    This class works as game constructer work with turtle to draw and store the require information
    to track the current status of the game.
    """
    def __init__(self) -> None:
        self.colors = ["red", "blue", "green", "yellow", "purple", "black"]
        self.button_names = ["checkbutton.gif", "file_error.gif", "leaderboard_error.gif",
                 "Lose.gif", "quit.gif", "quitmsg.gif", "winner.gif",
                   "xbutton.gif", "lackcolor.gif", "muticlick.gif"]
        self.secrete_code = self.generate_color_code() # secrete colorcode
        self.y_position = self.y_position_generator(340, 55)
        self.each_row = [] # Stroe ten Marble instances, each serve one row only move in x direction.
        self.x_position = [-305, -245, -185, -125] # Marble instance move instruction
        self.indicators = [] # Store ten Marble instance, move in x, y direction to form 2*2 indicator grid.
        self.x_indicator = [0, 10]
        self.y_indicator = [y + 22 for y in self.y_position] # make them more align with each other by position adjust
        # The container of six marble instance each contains different color (control marble)
        self.bottom_marble_collection = []
        self.current_row = 0 # Keep track which row user is working on
        self.col_next = 1 # Keep track what is next x_position to call
        self.colorcode = [] # Keep track User's colorcode choice update for each row
        self.endtrack = False # Flag to determine when the game should end
        self.best_score = None # Use to see whether we should update our leadboard.txt file
    
    def errorset(self):
        self.error = turtle.Turtle()# Message display turtle
        self.error.hideturtle() # Only showturtle() with specific condition and shape


    def generate_color_code(self):
        """
        Return a random generated secrete color code using random number generator

        The secrete color code does not allow repitition.
        """
        color_copy = self.colors[:]
        secrete_code = []
        while len(secrete_code) < 4:
            pick = random.randint(0, (len(color_copy) - 1))
            secrete_code.append(color_copy[pick])
            del color_copy[pick] # Prevent repitition occur
        return secrete_code
    
    def y_position_generator(self, starter, gap):
        """
        Return a arithmatic sequence in list format.

        Inputs are the starting y position (first row) and gap distance.

        Return the y_position of ten rowes.
        """
        result = [starter]
        for i in range(9):
            result.append(result[i] - gap)
        return result
    
    def draw_rect(self, x, y, length, width, pencolor = None, penwidth = None):
        """
        This function will draw a rectangle or square.

        The input requires start location of top-left corner(x,y), length and width of rect.

        There is no return value.
        """
        drawer = turtle.Turtle()
        drawer.speed(0)
        drawer.hideturtle()
        # reminder: penwidth = 10 is somewhat thick, 20 is very, 1 is thin line
        if pencolor:
            drawer.pencolor(pencolor)
        if penwidth:
            drawer.pensize(penwidth)
        drawer.penup()
        drawer.goto(x,y)
        drawer.setheading(0)
        instruction = [length, width, length, width]
        drawer.pendown()
        for distance in instruction:
            drawer.forward(distance)
            drawer.right(90)
        drawer.penup()

    def rect_setup(self):
        """
        create a rectangle structure for the game
        The current three start points are 
        Top left rectangle: (-415, 410) -- main game display
        Top right rectangle: (155, 410) -- leader display
        Bottom rectangle: (-415 to 415, -230 to -390) -- game control panel
        Each rectangle serves different purpose
        """
        self.draw_rect(-415, 410, 530, 620, "black", 10)
        self.draw_rect(155, 410, 260, 620, "purple", 8)
        self.draw_rect(-415, -230, 830, 160, "orange", 10)
        self.errorset()
        
    def top_left_setup(self):
        """
        This function will first creates and store 10 interaction marbles
        and draw a 10*4 game board to display user color selection.

        Then create another 10 indicator marbles and draw 10 sets of 2*2 
        indicator to tell the user result of their color code.
        """
        for y in self.y_position:
            self.each_row.append(m.Marble(0,y,"black", 20, False))
        for row in self.each_row:
            for x in self.x_position: # Interaction marbles will end at right most x_position
                row.x = x
                row.draw()
        for y in self.y_indicator:
            self.indicators.append(m.Marble(0,y,"black", 4, False))
        for indicator in self.indicators:
            for x in self.x_indicator: # Indicator marbels will end at top right most x_indicator
                indicator.x = x
                indicator.draw()
                indicator.y = indicator.y - 10
                indicator.draw()
                indicator.y = indicator.y + 10
        # After construction we need to move marbles to begining position -- left most
        self.order_correction()
    
    def order_correction(self):
        """
        this function will navigate both each_row and indicators to left most x value.
        """
        for row in self.each_row:
            row.x = self.x_position[0]
        for indicator in self.indicators:
            indicator.x = self.x_indicator[0]

    def row_reset(self, y):
        """
        Function reconstructs row depend on the y position given.
        """
        self.y_position
        index = self.y_position.index(y) # index is in [0,9] tells which row we wanna reconstruct
        self.each_row[index].erase() # clear all drawing of a specific (depend on y_position) interaction marble.
        self.each_row[index].fill = False # Draw circle and not fill color
        for x in self.x_position:
            self.each_row[index].x = x
            self.each_row[index].draw()
        self.order_correction() # Move back to left most position

    def line_aligner(self):
        """
        with a rectangle outline for each row, it makes user easier to 
        identify which row that they are working on.
        """
        drawer = turtle.Turtle()
        drawer.hideturtle()
        drawer.speed(0)
        drawer.setheading(0)
        aligner_position = self.y_position_generator(385, 55)
        for y in aligner_position:
            self.draw_rect(-330, y, 400, 50)

    def bottom_set(self, x = -370, y = -330):
        """
        This function creates six fixed position control marble and bottom buttons.
        """
        # Starting position -- y value will not change only x changes
        for color in self.colors:
            self.bottom_marble_collection.append(m.Marble(x, y, color=color, size=22))
            x = x + 55 # Distance betweeen each control marble
        for marble in self.bottom_marble_collection:
            marble.draw()

        self.button_set()# load all the gif into turtle

    def reset_bottom(self):
        """
        This function resets all six control marbles.
        """
        for marble in self.bottom_marble_collection:
            marble.erase()
            marble.deactivate = False # Control mable only clickable when deactivate=False
            marble.draw()
    def button_set(self):
        """
        This function will first register all the gif into turtle.

        Then set all the button inside of game control panel.
        """
        for button in self.button_names:
            turtle.register_shape(button)
        button1 = turtle.Turtle()
        button2 = turtle.Turtle()
        button3 = turtle.Turtle()
        button1.penup()
        button1.speed(0)
        button2.penup()
        button2.speed(0)
        button3.penup()
        button3.speed(0)
        button1.goto(110, -305)
        button1.shape("xbutton.gif") # change turtle shape to gif
        button2.goto(20, -305)
        button2.shape("checkbutton.gif")
        button3.goto(300, -311)
        button3.shape("quit.gif")
    
    def check_user(self, colorcode = None):
        """
        Function takes in user's color code and return number of red and black peg.

        This function takes a list of color code.

        Return number of red pegs and black pegs.
        """
        if (colorcode == None) or (not isinstance(colorcode, list)) or (len(colorcode) != 4):
            colorcode = self.colorcode
        test_secrete = self.secrete_code[:]
        red = 0
        black = 0
        for i in range(len(colorcode)):
            # Only works when repetition color is not allow
            if colorcode[i] in test_secrete:
                if colorcode[i] == test_secrete[i]:
                    black += 1
                else:
                    red += 1
        return red, black
    
    def show_indicators(self, red, black, marble):
        """
        This function will randomly assign red and black pegs into 2*2 indicator grid.

        Input: number of red and black pegs. The specific indicator that will draw pegs.
        """
        marble.fill = True
        y = marble.y
        result = ["red"]*red + ["black"]*black
        random.shuffle(result) # shuffle the order of red and black pegs
        # All (x,y) position of that specific indicator marble instance.
        all_combination = [[self.x_indicator[0], y], [self.x_indicator[1], y],
                            [self.x_indicator[0], y-10], [self.x_indicator[1], y-10]]
        for i in range(len(result)): # The fill order is left to right, top to bottom
            marble.color = result[i]
            marble.x = all_combination[i][0]
            marble.y = all_combination[i][1]
            marble.draw()
        
    def gameon(self):
        """Draw the board!"""
        self.rect_setup()
        self.top_left_setup()
        self.line_aligner()
        self.bottom_set()