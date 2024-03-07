"""


This file we do the test based on one generated secrete code (answer), 
and five random generated guess code, we will test to see whether 
our function performs as expected.
"""

import unittest
import random
from gamecons import GameConstructor
random.seed(1) # Set our secrete color code unchange for later test use
game = GameConstructor() 
the_answer = game.secrete_code # ['blue', 'black', 'red', 'yellow'] The answer.

guesses = [] # This will contains five random generated color codes, and we will check them with checkuser()
# Here is the key [['red', 'purple', 'black', 'green'], ['black', 'yellow', 'blue', 'red'], 
#                  ['yellow', 'red', 'black', 'green'], ['purple', 'red', 'black', 'green'], ['black', 'blue', 'red', 'yellow']]
for i in range(5):
    guesses.append(game.generate_color_code())

class MasterGameTest(unittest.TestCase):
    
    def test_checkuser(self):
        """
        We are testing the checkuser() function. This function will return two values:
            The first value is number of red pegs -- right color but wrong position.
            The second value is number of black pegs -- right color and right position.
        """
        self.assertEqual(game.check_user(the_answer), (0,4)) # This should always be 0 red and 4 black.
        self.assertEqual(game.check_user(guesses[0]), (2,0)) # check key of guesses to see
        self.assertEqual(game.check_user(guesses[1]), (4,0))
        self.assertEqual(game.check_user(guesses[2]), (3,0))
        self.assertEqual(game.check_user(guesses[3]), (2,0))
        self.assertEqual(game.check_user(guesses[4]), (2,2))


if __name__ == "__main__":
    unittest.main(exit=False)