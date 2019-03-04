from server_con import *
from board_tile import *
from random import random
from board import Board

# auxiliary files for roxxor strategy
from world_rep import get_all_paths, get_potential_targets, dist
from orders_tree import order_node

    
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
        faction = BoardTile.ally_faction
        enemy_faction = Faction.VAMP if faction==Faction.WERE else Faction.WERE
        
        tiles_of_interest = board.get_tiles_of_interest()
        
        our_tiles = tiles_of_interest[faction]
        enemy_tiles = tiles_of_interest[enemy_faction]
        
        all_paths = []
        for source in our_tiles:
            potential_targets = get_potential_targets(source, enemy_tiles, tiles_of_interest[Faction.HUM])
            all_paths += get_all_paths(source, enemy_tiles, potential_targets)
        
        pre_required = {t.id:0 for t in our_tiles}  # at first we don't require any troops from any of our tiles
        
        
        order_tree = order_node([], [], pre_required, all_paths, verbose=False)
        order_tree.create_sons()
        best_gain, best_son = order_tree.get_best_gain()
        

        if best_gain==0:
            return [[]]
        else:
            moves = []
            for i in range(len(best_son.assigned_paths)):
                source_tile = best_son.assigned_paths[i].source
                x = source_tile.x
                y = source_tile.y
                target_x = best_son.assigned_paths[i].dests[0].x
                target_y = best_son.assigned_paths[i].dests[0].y
                
                nb = best_son.assigned_nb[i]
                if best_son.required[source_tile.id] < source_tile.nb:
                    nb+=source_tile.nb-best_son.required[source_tile.id]  # leave no man behind
                    best_son.required[source_tile.id] = source_tile.nb
                
                dest_x = x+1 if target_x>x else x-1 if target_x<x else x
                dest_y = y+1 if target_y>y else y-1 if target_y<y else y
                moves += [(x,y,nb, dest_x, dest_y)]
        return moves
        

if __name__ == '__main__':
    game_client = GameClient()
    game_client.start_connection()
