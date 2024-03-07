"""
Zeyu Li
FALL2023, CS5001
Final project
This file defined onclick event, and glue all other classes together.
"""

from Pointer import Pointer
from datetime import datetime
from gamecons import GameConstructor
from file_process import AllFile
from myscreen import GameScreen

class Mastermind:
    """
    Define onlick event and call all pre-defined classes and glue them together to make game run.
    """
    
    def __init__(self) -> None:
        self.gamescreen = GameScreen() # The class contains all screen related action.
        self.pointer = Pointer(-370, 360) # The Pointer instance that navigate the arrow self.pointer in GUI
        self.game = GameConstructor() # This class contains turtle game related
        self.keep = AllFile() # This class contains file read and write (append) related

    def action(self, x, y):
        """
        Function that runs everytime onclick event happens.

        The input is the (x,y) position that user clicked on turtle.Screen.

        The function will have different effect depend on click position and self.game status.
        """
        self.game.error.hideturtle()
        if self.game.endtrack:
            self.gamescreen.screen.exitonclick()
        else: 
            #Bottom rectangle: (-415 to 415, -230 to -390) the only interaction zone we need self.keep track
            if x > -415 and x < 415 and y < -230 and y > -390: # Only zone user click matter
                if x > -400 and x < -70 and y > -335 and y < -280: # where six control marbles exist
                    for colorball in self.game.bottom_marble_collection:
                        if self.game.col_next > len(self.game.x_position):
                            break
                        elif colorball.clicked_in_region(x,y) and not colorball.deactivate: # more detail in Marble Class
                            self.game.each_row[self.game.current_row].fill = True
                            self.game.each_row[self.game.current_row].color = colorball.color
                            self.game.colorcode.append(colorball.color)
                            self.game.each_row[self.game.current_row].draw()
                            colorball.draw_empty()
                            colorball.deactivate = True # deactivate used control marble
                            if self.game.col_next >= len(self.game.x_position):
                                self.game.col_next += 1
                                break # We reached end of row, click on control marble should do nothing
                            self.game.each_row[self.game.current_row].x = self.game.x_position[self.game.col_next]
                            self.game.col_next += 1 # Going to next x_position

                # The region of xbutton, should perform reset of current row
                elif x > 75 and x < 145 and y > -333 and y < -270:
                    self.game.col_next = 1 # reset next x_position
                    self.game.colorcode.clear() # reset colorcode
                    self.game.row_reset(self.game.y_position[self.game.current_row]) # reset current interaction marble
                    self.game.reset_bottom() # reset current control marble

                elif x > -12 and x < 50 and y > -333 and y < -270:# green check button
                    if len(self.game.colorcode) < len(self.game.x_position): # user has not select 4 color but try to submit color code
                        self.game.error.shape("lackcolor.gif")
                        self.game.error.showturtle()
                    else:
                        if len(set(self.game.colorcode)) != 4 or len(self.game.colorcode) > 4: # The muticlick deficency occurred need to reset current row
                            self.game.col_next = 1
                            self.game.colorcode.clear()
                            self.game.row_reset(self.game.y_position[self.game.current_row])
                            self.game.reset_bottom()
                            with open("mastermind_errors.err", mode="a") as report: # record the error happenned
                                now = datetime.now()
                                report.write("At "+ str(now) + " Muti-Click error occurred which causing duplicated "
                                            "color in color code, so row_reset() is called.\n")
                            self.game.error.shape("muticlick.gif")
                            self.game.error.showturtle()
                        else:
                            self.game.col_next = 1
                            self.game.reset_bottom()
                            red, black = self.game.check_user()
                            self.game.show_indicators(red, black, self.game.indicators[self.game.current_row])
                            if black == 4: # User colorcode == secrete_code
                                self.game.endtrack = True # End the self.game flag on
                                self.game.error.shape("winner.gif")
                                self.game.error.showturtle()
                                self.game.best_score = self.game.current_row + 1 # convert from 0-9 to 1-10
                                self.keep.the_record_update(self.gamescreen.username, self.game.best_score) # Only win can trigger this function
                            else:
                                if self.game.current_row >= 9: # Used all 10 chances
                                    self.game.error.shape("Lose.gif")
                                    self.game.error.showturtle()
                                    self.game.endtrack = True
                                    solution = " , ".join(self.game.secrete_code)
                                    solution = "[" + solution + "]"
                                    # Show the user the corrent solution
                                    self.gamescreen.screen.textinput("Here is the secrete color code", solution)
                                else:
                                    # Not correct but there are still chance left
                                    self.game.colorcode.clear()
                                    self.pointer.next(55)
                                    self.game.current_row += 1
                elif x > 200 and x < 400 and y > -365 and y < -250: # The quit button
                    self.game.error.shape("quitmsg.gif")
                    self.game.error.showturtle()
                    self.game.endtrack = True
        
    def leader_board(self):
        """
        Function will try to read leadboard.txt and store the info into a dictionary.
        If the file does not found, we will generate a new file and update the .err file.
        """
        try:
            with open("leaderboard.txt", "r") as records:
                for record in records:
                    self.keep.MVP.append(record)
                    result = record.split(":")
                    self.keep.current_record[(result[0].upper()+":")] = int(result[1].strip("\n"))
        except Exception as e:
            self.game.error.shape("leaderboard_error.gif")
            self.game.error.showturtle()
            with open("mastermind_errors.err", mode= "a") as report:
                now = datetime.now()
                report.write("At "+ str(now)+ f" {e} leaderboard.txt not found a new one is created.\n")

            with open("leaderboard.txt", mode="w"): # create the file but do nothing
                pass


    def clickon(self):
        """
        Function that start the onclick events.
        """
        try:
            self.gamescreen.screen.onclick(self.action)
        except Exception as e:
            with open("mastermind_errors.err", mode="a") as report:
                now = datetime.now()
                report.write("At " + str(now) + f" {e} User abnormally play the self.game"
                            " causing backend can not follow and update in time.\n")


    def launcher(self):
        """
        This function will call all the required function to make self.game run
        """
        try:
            self.game.gameon()
            self.leader_board()
            self.keep.show_leader_board()
            self.clickon()
        except Exception as e:
            with open("mastermind_errors.err", mode="a") as report:
                now = datetime.now()
                report.write("At " + str(now) + f" {e} an unexpected error occur when launching, please break down to see why.\n")

