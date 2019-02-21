from server_con import *
from board_tile import *
from random import random

class GameClient():
    def __init__(self):
        self.__board = [[]]
        self.__connection = ServerCon(self)
        self.__n = 0
        self.__m = 0
        self.__us = ""  # equals "VAMP" or "WERE"
        
    """ Start everything, including connection """
    def start(self, ):
        
    """ All callbacks from the server, receiving formated input """
    def callback_set(self, n, m):
        

    def callback_hum(self, ):
        

    def callback_hme(self, ):
        

    def callback_map(self, ):
        

    def callback_upd(self, ):
        

    def callback_end(self, ):
        

    def callback_bye(self, ):
        
        
    def decide(self):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = [board_tile for row in self.__board for board_tile in row
                             if board_tile.type == self.__us]
        
        
        random_tile = random.choice(our_tiles)  # awesome IA algorithm
        x = random_tile.x
        y = random_tile.y
        n = random_tile.n
        
        pot_dest = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
        
        
        dest_x, dest_y = random.choice([(i,j) for (i,j) in pot_dest if i>=0 and i<self.__n and j >=0 and j<self.__m])
        random_n = random.choice(list(range(1,n+1)))

        return [[x,y,random_n, dest_x, dest_y]]
        

if __name__ == '__main__':
    game_client = GameClient()
    game_client.start()
