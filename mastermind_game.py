"""
Zeyu Li
CS5001, FALL2023
This file simply call Mastermind class and activate the game.
"""
import turtle
from Mastermind import Mastermind

def main():
    thegame = Mastermind()
    thegame.launcher() # 3, 2, 1 launch!
    turtle.mainloop()
if __name__ == "__main__":
    main()