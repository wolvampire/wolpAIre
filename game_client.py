from server_con import *
from board_tile import *
from decider import *
from board import Board
from roxxor import *
import time

# auxiliary files for roxxor strategy
from world_rep import get_all_paths, get_potential_targets, dist
from orders_tree import order_node

    
class GameClient():
    def __init__(self):
        self.__decider = Decider()
        self.start()

    def start_connection(self):
        self.__connection = ServerCon(self)
        self.__connection.connect_to_server("127.0.0.1", 6666)
        self.__connection.send_nme(self.__decider.get_name())
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

    def give_decider(self, decider):
        self.__decider = decider

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
        update_success = self.update_map(changesInfosList)
        if update_success:
            print("Waiting ...")
            time.sleep(1)
            print("Computing ...")
            moves = self._decide()
            print("Computing done.")
            self.__connection.send_mov(moves)
        else:
            print("Failed update, did not decide.")
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

        
    def _decide(self):
        return self.__decider.decide(self.__board)


if __name__ == '__main__':
    import closest
    game_client = GameClient()
    game_client.give_decider(roxxor())
    game_client.start_connection()
