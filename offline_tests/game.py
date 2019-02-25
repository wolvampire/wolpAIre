from random import random
from random import randint
import random

from time import time
import sys
import os 

from board_tile import board_tile


class game():
    def __init__(self, id_game, n, m):
        self.__board = [[]]
        self.__n = n
        self.__m = m
        self.id_game = id_game
        self.orders
        self.init_random_state = random.getstate()  # to get the same results later when we reload the game and re-simulate the orders
        self.prng = random.Random()
        print(prng.random())
    
    
    def create_board(self):
        self.__board = [[board_tile(x,y,randint(1,10),"HUM") if random()<P_hum else board_tile(x,y) for y in range(self.__m)] for x in range(self.__n)]
       
        self.__board[1][1]=board_tile(1,1,10,"WERE")
        self.__board[self.__n-2][self.__m-2]=board_tile(self.__n-2,self.__m-2,10,"VAMP")
        
        
    def get_board(self):
        return self.__board
        
        
    def reload(self):
        self.prng.setstate(self.init_random_state)
        print(prng.random())
        