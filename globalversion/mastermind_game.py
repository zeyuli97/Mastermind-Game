import Marble as m
import random
import turtle
import Pointer
from datetime import datetime

# store colors in global frame make easier access
colors = ["red", "blue", "green", "yellow", "purple", "black"]
# All the gif images we will use later.
button_names = ["checkbutton.gif", "file_error.gif", "leaderboard_error.gif",
                 "Lose.gif", "quit.gif", "quitmsg.gif", "winner.gif",
                   "xbutton.gif", "lackcolor.gif", "muticlick.gif"]
# The screen we will use to terminate the turtle.
screen = turtle.Screen()
username = screen.textinput("Please enter your username here: ",
                             "Not CaSe SenSitiVe:)")
# Make user check non-case sensative
try:
    username = username.upper()
    username += ":" # For better looking and easier split()
except Exception as e:
    username = "Untrackable user:".upper()
    now = datetime.now()
    with open("mastermind_errors.err", mode="a") as report:
        report.write("At " + str(now) + f" {e} due to user does not give a valid player name -- name them untrackable user.\n")


def generate_color_code():
    """
    Return a random generated secrete color code using random number generator

    The secrete color code does not allow repitition.
    """
    color_copy = colors[:]
    secrete_code = []
    while len(secrete_code) < 4:
        pick = random.randint(0, (len(color_copy) - 1))
        secrete_code.append(color_copy[pick])
        del color_copy[pick] # Prevent repitition occur
    return secrete_code

secrete_code = generate_color_code() # Generate the secrete solution code

def y_position_generator(starter, gap):
    """
    Return a arithmatic sequence in list format.

    Inputs are the starting y position (first row) and gap distance.

    Return the y_position of ten rowes.
    """
    result = [starter]
    for i in range(9):
        result.append(result[i] - gap)
    return result

def draw_rect(x, y, length, width, pencolor = None, penwidth = None):
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

def rect_setup():
    """
    create a rectangle structure for the game
    The current three start points are 
    Top left rectangle: (-415, 410) -- main game display
    Top right rectangle: (155, 410) -- leader display
    Bottom rectangle: (-415 to 415, -230 to -390) -- game control panel
    Each rectangle serves different purpose
    """
    draw_rect(-415, 410, 530, 620, "black", 10)
    draw_rect(155, 410, 260, 620, "purple", 8)
    draw_rect(-415, -230, 830, 160, "orange", 10)

each_row = [] # Stroe ten Marble instances, each serve one row only move in x direction.
x_position = [-305, -245, -185, -125] # Marble instance move instruction
y_position = y_position_generator(340, 55)
indicators = [] # Store ten Marble instance, move in x, y direction to form 2*2 indicator grid. 
x_indicator = [0, 10]
y_indicator = [y + 22 for y in y_position] # make them more align with each other by position adjust
def top_left_setup():
    """
    This function will first creates and store 10 interaction marbles
    and draw a 10*4 game board to display user color selection.

    Then create another 10 indicator marbles and draw 10 sets of 2*2 
    indicator to tell the user result of their color code.
    """
    for y in y_position:
        each_row.append(m.Marble(0,y,"black", 20, False))
    for row in each_row:
        for x in x_position: # Interaction marbles will end at right most x_position
            row.x = x
            row.draw()
    for y in y_indicator:
        indicators.append(m.Marble(0,y,"black", 4, False))
    for indicator in indicators:
        for x in x_indicator: # Indicator marbels will end at top right most x_indicator
            indicator.x = x
            indicator.draw()
            indicator.y = indicator.y - 10
            indicator.draw()
            indicator.y = indicator.y + 10
    # After construction we need to move marbles to begining position -- left most
    order_correction()
    
def order_correction():
    """
    this function will navigate both each_row and indicators to left most x value.
    """
    for row in each_row:
        row.x = x_position[0]
    for indicator in indicators:
        indicator.x = x_indicator[0]

def row_reset(y):
    """
    Function reconstructs row depend on the y position given.
    """
    global y_position
    index = y_position.index(y) # index is in [0,9] tells which row we wanna reconstruct
    each_row[index].erase() # clear all drawing of a specific (depend on y_position) interaction marble.
    each_row[index].fill = False # Draw circle and not fill color
    for x in x_position:
        each_row[index].x = x
        each_row[index].draw()
    order_correction() # Move back to left most position
    

def line_aligner():
    """
    with a rectangle outline for each row, it makes user easier to 
    identify which row that they are working on.
    """
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.speed(0)
    drawer.setheading(0)
    aligner_position = y_position_generator(385, 55)
    for y in aligner_position:
        draw_rect(-330, y, 400, 50)
    
# The Pointer instance that navigate the arrow pointer in GUI
pointer = Pointer.Pointer(-370, 360)

# The container of six marble instance each contains different color (control marble)
bottom_marble_collection = []
def bottom_set():
    """
    This function creates six fixed position control marble.
    """
    # Starting position -- y value will not change only x changes
    y = -330
    x = -370
    for color in colors:
        bottom_marble_collection.append(m.Marble(x, y, color=color, size=22))
        x = x + 55 # Distance betweeen each control marble
    for marble in bottom_marble_collection:
        marble.draw()

def reset_bottom():
    """
    This function resets all six control marbles.
    """
    for marble in bottom_marble_collection:
        marble.erase()
        marble.deactivate = False # Control mable only clickable when deactivate=False
        marble.draw()

def button_set(button_names):
    """
    This function will first register all the gif into turtle.

    Then set all the button inside of game control panel.
    """
    for button in button_names:
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

def check_user(colorcode):
    """
    Function takes in user's color code and return number of red and black peg.

    This function takes a list of color code.

    Return number of red pegs and black pegs.
    """
    test_secrete = secrete_code[:]
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

def show_indicators(red, black, marble):
    """
    This function will randomly assign red and black pegs into 2*2 indicator grid.

    Input: number of red and black pegs. The specific indicator that will draw pegs.
    """
    marble.fill = True
    y = marble.y
    result = ["red"]*red + ["black"]*black
    random.shuffle(result) # shuffle the order of red and black pegs
    # All (x,y) position of that specific indicator marble instance.
    all_combination = [[x_indicator[0], y], [x_indicator[1], y], [x_indicator[0], y-10], [x_indicator[1], y-10]]
    for i in range(len(result)): # The fill order is left to right, top to bottom
        marble.color = result[i]
        marble.x = all_combination[i][0]
        marble.y = all_combination[i][1]
        marble.draw()


button_set(button_names) # load all the gif into turtle
error = turtle.Turtle() # Message display turtle
error.hideturtle() # Only showturtle() with specific condition and shape

current_row = 0 # Keep track which row user is working on
col_next = 1 # Keep track what is next x_position to call
colorcode = [] # Keep track User's colorcode choice update for each row
endtrack = False # Flag to determine when the game should end
best_score = None # Use to see whether we should update our leadboard.txt file

def action(x, y):
    """
    Function that runs everytime onclick event happens.

    The input is the (x,y) position that user clicked on turtle.Screen.

    The function will have different effect depend on click position and game status.
    """
    global col_next
    global current_row
    global endtrack
    global best_score
    error.hideturtle()
    if endtrack:
        screen.exitonclick()
        
    #Bottom rectangle: (-415 to 415, -230 to -390) the only interaction zone we need keep track
    if x > -415 and x < 415 and y < -230 and y > -390: # Only zone user click matter
        if x > -400 and x < -70 and y > -335 and y < -280: # where six control marbles exist
            for colorball in bottom_marble_collection:
                if col_next > len(x_position):
                    break
                elif colorball.clicked_in_region(x,y) and not colorball.deactivate: # more detail in Marble Class
                    each_row[current_row].fill = True
                    each_row[current_row].color = colorball.color
                    colorcode.append(colorball.color)
                    each_row[current_row].draw()
                    colorball.draw_empty()
                    colorball.deactivate = True # deactivate used control marble
                    if col_next >= len(x_position):
                        col_next += 1
                        break # We reached end of row, click on control marble should do nothing
                    each_row[current_row].x = x_position[col_next]
                    col_next += 1 # Going to next x_position

        # The region of xbutton, should perform reset of current row
        elif x > 75 and x < 145 and y > -333 and y < -270:
            col_next = 1 # reset next x_position
            colorcode.clear() # reset colorcode
            row_reset(y_position[current_row]) # reset current interaction marble
            reset_bottom() # reset current control marble

        elif x > -12 and x < 50 and y > -333 and y < -270:# green check button
            if len(colorcode) < len(x_position): # user has not select 4 color but try to submit color code
                error.shape("lackcolor.gif")
                error.showturtle()
            else:
                if len(set(colorcode)) != 4 or len(colorcode) > 4: # The muticlick deficency occurred need to reset current row
                    col_next = 1
                    colorcode.clear()
                    row_reset(y_position[current_row])
                    reset_bottom()
                    with open("mastermind_errors.err", mode="a") as report: # record the error happenned
                        now = datetime.now()
                        report.write("At "+ str(now) + " Muti-Click error occurred which causing duplicated "
                                     "color in color code, so row_reset() is called.\n")
                    error.shape("muticlick.gif")
                    error.showturtle()
                else:
                    col_next = 1
                    reset_bottom()
                    red, black = check_user(colorcode)
                    show_indicators(red, black, indicators[current_row])
                    if black == 4: # User colorcode == secrete_code
                        endtrack = True # End the game flag on
                        error.shape("winner.gif")
                        error.showturtle()
                        best_score = current_row + 1 # convert from 0-9 to 1-10
                        the_record_update() # Only win can trigger this function
                    else:
                        if current_row >= 9: # Used all 10 chances
                            error.shape("Lose.gif")
                            error.showturtle()
                            endtrack = True
                            solution = " , ".join(secrete_code)
                            solution = "[" + solution + "]"
                            # Show the user the corrent solution
                            screen.textinput("Here is the secrete color code", solution)
                        else:
                            # Not correct but there are still chance left
                            colorcode.clear()
                            pointer.next(55)
                            current_row += 1
        elif x > 200 and x < 400 and y > -365 and y < -250: # The quit button
            error.shape("quitmsg.gif")
            error.showturtle()
            endtrack = True
    

MVP = [] # Store the info of leadboard.txt for later use
current_record = {} # key is name value is bestscore
def leader_board():
    """
    Function will try to read leadboard.txt and store the info into a dictionary.
    If the file does not found, we will generate a new file and update the .err file.
    """
    global current_record
    global MVP
    try:
        with open("leaderboard.txt", "r") as records:
            for record in records:
                MVP.append(record)
                result = record.split(":")
                current_record[(result[0].upper()+":")] = int(result[1].strip("\n"))
    except Exception as e:
        error.shape("leaderboard_error.gif")
        error.showturtle()
        with open("mastermind_errors.err", mode= "a") as report:
            now = datetime.now()
            report.write("At "+ str(now)+ f" {e} leaderboard.txt not found a new one is created.\n")

        with open("leaderboard.txt", mode="w"): # create the file but do nothing
            pass

def the_record_update():
    """
    Function will only be called if user wins the game.
    Function will check if the user won before, if so keep the lower score.
    After updating, we will rewrite the leaderboard.txt.
    """
    global current_record
    try:
        if username in current_record:
            if best_score < current_record[username]:
                current_record[username] = best_score
        else:
            current_record[username] = best_score

        with open("leaderboard.txt", mode="w") as new_record:
            for key, value in current_record.items():
                new_record.write(f"{key} {value}\n")
    
    except Exception as e:
        with open("leaderboard.txt", mode="w") as records:
            records.write(f"{username} {best_score}\n")
        with open("mastermind_errors.err", mode="a") as report:
            now = datetime.now()
            report.write("At " + str(now) + f" {e} the_record_update() function"
                         " occurred an error and leadboard.txt is rewrited.\n")

score = turtle.Turtle() # This turtle will use to show the leader scores
score.up()
score.hideturtle()
score.goto(180, 375)
score.color("blue")

def show_leader_board():
    """
    Function write all the leaderboard.txt on the turtle.Screen.
    Due to space limitation, we will only show first 18 users on file.
    """
    x = 180
    y = 320
    score.write("Leaders:", font=("Verdana", 26, "normal"))
    for i in range(min(len(MVP), 18)): # Only first 18 users will be shown.
        score.goto(x, y)
        score.write(MVP[i], font=("Verdana", 17, "normal"))
        y -= 30

def game():
    """
    Function that start the onclick events.
    """
    try:
        screen.onclick(action)
    except Exception as e:
        with open("mastermind_errors.err", mode="a") as report:
            now = datetime.now()
            report.write("At " + str(now) + f" {e} User abnormally play the game"
                         " causing backend can not follow and update in time.\n")

def main():
    try:
        rect_setup()
        top_left_setup()
        line_aligner()
        bottom_set()
        leader_board()
        show_leader_board()
        game()
    except Exception as e:
        with open("mastermind_errors.err", mode="a") as report:
            now = datetime.now()
            report.write("At " + str(now) + f" {e} an unexpected error occur when running main(), please break down to see why.\n")
if __name__ == "__main__":
    main()
