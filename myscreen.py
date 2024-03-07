"""
Zeyu Li
Fall2023, CS5001
Final Project
This file contains GameScreen class
"""

import turtle
from datetime import datetime

class GameScreen:
    """
    This class will handle all the turtle.Screen() related things.
    """
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.screensize(400, 300)
        self.username = self.screen.textinput("Please enter your username here: ",
                             "Do not worry Not CaSe SenSitiVe :)")
        try:
            self.username = self.username.upper() # Make username not case sensitive
            if self.username == "":
                self.username = "Empty name".upper()
            self.username += ":" # For better looking and easier split()
        except Exception as e:
            self.username = "Untrackable user:".upper()
            now = datetime.now()
            with open("mastermind_errors.err", mode="a") as report:
                report.write("At " + str(now) + f" {e} due to user does not give a valid player name -- name them untrackable user.\n")
