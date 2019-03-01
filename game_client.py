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
        self.start()
        self.__board = Board(m, n)
        return True

    def callback_hum(self, housesCoordinates):
        for (x,y) in housesCoordinates:
            self.__board.tile(x, y).faction = Faction.HUM
        return True

    def callback_hme(self, x, y):
        self.__startingHome = [x, y]
        return True

    def callback_upd(self, changesInfosList):
        update_success =  self.update_map(changesInfosList)
        if update_success:
            moves = self.decide()
            print(self.__board)
            self.__connection.send_mov(moves)
        return update_success

    def callback_map(self, tilesInfosList):
        return_value = self.update_map(tilesInfosList)
        print(self.__board)
        start_tile_faction = self.__board.tile(self.__startingHome[0], self.__startingHome[1]).faction
        assert start_tile_faction in [Faction.VAMP, Faction.WERE], start_tile_faction
        BoardTile.ally_faction = start_tile_faction
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
            print("Received order : {}".format(change))
            # checks that there is no couple of faction on a single tile
            assert (nHum*nVamp == 0) and (nHum*nWere == 0) and (nVamp*nWere == 0)
            if nHum != 0:
                self.__board.tile(x,y).nb = nHum
                self.__board.tile(x,y).faction = Faction.HUM
                print("Added {} humans.".format(nHum))
            elif nVamp != 0:
                self.__board.tile(x,y).nb = nVamp
                self.__board.tile(x,y).faction = Faction.VAMP
                print("Added {} vampires.".format(nVamp))
            elif nWere != 0:
                self.__board.tile(x,y).nb = nWere
                self.__board.tile(x,y).faction = Faction.WERE
                print("Added {} werewolves.".format(nWere))
            else:
                self.__board.tile(x,y).nb = 0
                self.__board.tile(x,y).faction.EMPT
                print("Emptied tile.")
        print(self.__board)
        return True        
        
    def decide(self):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = self.__board.get_tiles_of_interest()[BoardTile.ally_faction]
        our_tile = our_tiles[0]
        x = our_tile.x
        y = our_tile.y
        nb = our_tile.nb
        
        human_tiles = self.__board.get_tiles_of_interest()[Faction.HUM]
        
        min_dist = self.__board.height + self.__board.width
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
