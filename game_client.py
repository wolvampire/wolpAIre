from server_con import *
from board_tile import *
from random import random
from board import Board

    
class GameClient():
    def __init__(self):
        self.start()

    def start_connection(self):
        self.__connection = ServerCon(self)
        self.__connection.connect_to_server("127.0.0.1", 6666)
        self.__connection.send_nme("test")
        while self.__connection.is_connected():
            self.__connection.listen()
        
    def start(self):
        '''
        reset for a new game
        '''
        
        self.__board = None
        self.__startingHome = []
        
            
    def callback_set(self, n, m):
        '''
        All callbacks from the server, receiving formated input
        '''
        self.__board = Board(m, n)
        return True

    def callback_hum(self, housesCoordinates):
        for (x,y) in housesCoordinates:
            self.__board.tile(x, y).faction = Faction.HUM

    def callback_hme(self, x, y):
        self.__startingHome = [x, y]
        return True

    def callback_upd(self, changesInfosList):
        update_success =  update_map(changesInfosList)
        if update_success:
            moves = self.decide()
            print(self.__board)
            self.__connection.send_mov(moves)
        return update_success

    def callback_map(self, tilesInfosList):
        return_value = update_map(tilesInfosList)
        assert self.__board.tile(self.__startingHome[0], self.__startingHome[1]).faction in [Faction.VAMP,Faction.WERE]
        BoardTile.ally_faction = self.__board.tile(self.__startingHome[0], self.__startingHome[1]).faction
        return return_value

    def callback_end(self):
        self.start()

    def callback_bye(self):
        pass
        #TODO @paternose

    def update_map(self, changesInfosList):
        for change in changesInfosList:
            x = change[0]
            y = change[1]
            nHum = change[2]
            nVamp = change[3]
            nWere = change[4]
            if (nHum*nVamp == 0) and (nHum*nWere == 0) and (nVamp*nWere == 0):
                #  checks that there is no couple of faction on a single tile
                if nHum != 0:
                    self.__board.tile(x,y).nb = nHum
                    self.__board.tile(x,y).faction.HUM
                if nVamp != 0:
                    self.__board.tile(x,y).nb = nVamp
                    self.__board.tile(x,y).faction.VAMP
                if nWere != 0:
                    self.__board.tile(x,y).nb = nWere
                    self.__board.tile(x,y).faction.WERE
            else :
                return False
        return True        
        
    def decide(self):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = self.__board.get_tiles_of_interest()[BoardTile.ally_faction]
        
        
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
    game_client.start_connection()
