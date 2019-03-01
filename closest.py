from decider import *



class ClosestDecider(Decider):
    def __init__(self):
        self._name = "Closest"

    def decide(self, board):
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
