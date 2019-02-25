from server_con import *
from board_tile import *
from random import random


    
class GameClient():
    def __init__(self):
        self.start()

    def start(self):
        '''
         Start everything, including connection
        '''
        self.__connection = ServerCon(self)
        self.__board = [[]]
        self.__n = 0
        self.__m = 0
        self.__startingHome = []
        self.__us = None  # equals "VAMP" or "WERE"
        
    def callback_set(self, n, m):
        '''
        All callbacks from the server, receiving formated input
        '''
        self.__board = [[board_tile(x,y) for y in range(m)] for x in range(n)]
        return True

    def callback_hum(self, nHouses, housesCoordinates):
        if nHouses == len(housesCoordinates):
            for (x,y) in housesCoordinates:
                self.__board[x][y] = board_tile(x,y,faction=Faction.HUM)
        else:
            return False
        return True

    def callback_hme(self, x, y):
        self.__startingHome = [x,y]
        self.__us = self.__board[x][y].faction
        return True

    def callback_upd(self, nChanges, changesInfosList):
        update_success =  update_map(self, nChanges, changesInfosList)
        if update_success:
            moves = self.decide()
            self.__connection.send_mov(moves)
        return update_success

    def callback_map(self, nTiles, tilesInfosList):
        return_value = update_map(self, nTiles, tilesInfosList)
        if self.__board[self.__startingHome[0]][self.__startingHome[1]].faction in [Faction.VAMP,Faction.WERE]:
            self.__us = self.__board[self.__startingHome[0]][self.__startingHome[1]].faction
        else:
            return False
        return return_value

    def callback_end(self):
        self.start()

    def callback_bye(self):
                                                        #TODO @paternose


    def update_map(self, nChanges, changesInfosList):
        if nChanges == len(changesInfosList):
            for change in changesInfosList:
                x = change[0]
                y = change[1]
                nHum = change[2]
                nVamp = change[3]
                nWere = change[4]
                if (nHum*nVamp == 0) and (nHum*nWere == 0) and (nVamp*nWere == 0):
                    #  checks that there is no couple of faction on a single tile
                    if nHum != 0:
                        self.__board[x][y] = board_tile(x,y,nb=nHum,faction=Faction.HUM)
                    if nVamp != 0:
                        self.__board[x][y] = board_tile(x,y,nb=nVamp,faction=Faction.VAMP)
                    if nWere != 0:
                        self.__board[x][y] = board_tile(x,y,nb=nWere,faction=Faction.WERE)
                else :
                    return False
        else:
            return False
        return True        
        
    def decide(self):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = [board_tile for row in self.__board for board_tile in row
                             if board_tile.faction == self.__us]
        
        
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
