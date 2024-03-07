"""
Zeyu Li
FALL2023, CS5001
Final Project
This class contains file processing related stuff.
"""
from datetime import datetime
import turtle

class AllFile:
    """
    This class read and update the leaderboard.txt.
    Also handle the situation that txt file not found.
    """
    def __init__(self) -> None:
        self.MVP = [] # Store the info of leadboard.txt for later use
        self.current_record = {} # key is name value is bestscore
        self.score = turtle.Turtle() # This turtle will use to show the leader scores
        self.score.up()
        self.score.hideturtle()
        self.score.goto(180, 375)
        self.score.color("blue")

    def show_leader_board(self, x = 180, y = 320):
        """
        Function write all the leaderboard.txt on the turtle.Screen.
        Due to space limitation, we will only show first 18 users on file.
        """
        self.score.write("Leaders:", font=("Verdana", 26, "normal"))
        for i in range(min(len(self.MVP), 18)): # Only first 18 users will be shown.
            self.score.goto(x, y)
            self.score.write(self.MVP[i], font=("Verdana", 17, "normal"))
            y -= 30
    
    def the_record_update(self, username, best_score):
        """
        Function will only be called if user wins the game.
        Function will check if the user won before, if so keep the lower score.
        After updating, we will rewrite the leaderboard.txt.
        """
        try:
            if username in self.current_record:
                if best_score < self.current_record[username]:
                    self.current_record[username] = best_score
            else:
                self.current_record[username] = best_score

            with open("leaderboard.txt", mode="w") as new_record:
                for key, value in self.current_record.items():
                    new_record.write(f"{key} {value}\n")
        
        except Exception as e:
            with open("leaderboard.txt", mode="w") as records:
                records.write(f"{username} {best_score}\n")
            with open("mastermind_errors.err", mode="a") as report:
                now = datetime.now()
                report.write("At " + str(now) + f" {e} the_record_update() function"
                            " occurred an error and leadboard.txt is rewrited.\n")
