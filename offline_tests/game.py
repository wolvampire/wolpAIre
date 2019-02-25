from random import random
from random import randint
import random

from time import time
import sys
import os 

from board_tile import board_tile


class game():
    def __init__(self, id_game):
        self.__board = [[]]
        self.__n = 0
        self.__m = 0
        self.id_game = id_game
        self.orders
        self.init_random_state = random.getstate()  # to get the same results later when we reload the game and re-simulate the orders


    def reload()
        random.setstate(self.init_random_state)
        print random.random()

        # You can also restore the state into your own instance of the PRNG, to avoid
        # thread-safety issues from using the default, global instance.
        prng = random.Random()
        prng.setstate(old_state)
        print prng.random()