from server_con import *
from board_tile import *

    
class GameClient():
    def __init__(self):
        self.start_connection()

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
        
        self.__board = [[]]
        self.__n = 0
        self.__m = 0
        self.__startingHome = []
        self.__us = None  # equals "VAMP" or "WERE"
        
            
    def callback_set(self, n, m):
        '''
        All callbacks from the server, receiving formated input
        '''
        self.start()
        self.__board = [[board_tile(x,y) for y in range(n)] for x in range(m)]
        print(self.__board)
        return True

    def callback_hum(self, housesCoordinates):
        for (x,y) in housesCoordinates:
            print("x : {}; y : {}".format(x, y))
            self.__board[x][y] = board_tile(x,y,faction=Faction.HUM)
        return True

    def callback_hme(self, x, y):
        self.__startingHome = [x,y]
        return True

    def callback_upd(self, changesInfosList):
        update_success =  self.update_map(changesInfosList)
        if update_success:
            moves = self.decide()
            self.__connection.send_mov(moves)
        return update_success

    def callback_map(self, tilesInfosList):
        return_value = self.update_map(tilesInfosList)
        if self.__board[self.__startingHome[0]][self.__startingHome[1]].faction in [Faction.VAMP,Faction.WERE]:
            self.__us = self.__board[self.__startingHome[0]][self.__startingHome[1]].faction
        else:
            print("Error callback_map : home faction is {}".format(self.__board[self.__startingHome[0]][self.__startingHome[1]].faction))
            return False
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
                    self.__board[x][y] = board_tile(x,y,nb=nHum,faction=Faction.HUM)
                if nVamp != 0:
                    self.__board[x][y] = board_tile(x,y,nb=nVamp,faction=Faction.VAMP)
                if nWere != 0:
                    self.__board[x][y] = board_tile(x,y,nb=nWere,faction=Faction.WERE)
            else :
                return False
        return True        
        
    def decide(self):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        print("self __us : {}".format(self.__us))
        our_tiles = [board_tile for row in self.__board for board_tile in row if board_tile.faction == self.__us]
        our_tile = our_tiles[0]
        x = our_tile.x
        y = our_tile.y
        nb = our_tile.nb
        
        human_tiles = [board_tile for row in self.__board for board_tile in row if board_tile.faction == Faction.HUM]
        
        min_dist = self.__n + self.__m
        target_x, target_y = (0,0)
        for tile in human_tiles:
            dist = max(abs(tile.x-our_tile.x), abs(tile.y-our_tile.y))
            if dist < min_dist and tile.nb < nb:
                min_dist = dist
                target_x, target_y = (tile.x, tile.y)
        
        dir_x = 1 if target_x>our_tile.x else -1 if target_x<our_tile.x else 0
        dir_y = 1 if target_y>our_tile.y else -1 if target_y<our_tile.y else 0
        
        return [[x,y,nb, our_tile.x+dir_x, our_tile.y+dir_y]]   
        

if __name__ == '__main__':
    game_client = GameClient()
    game_client.start_connection()
