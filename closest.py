from decider import *
from board import *
from board_tile import *


class ClosestDecider(Decider):
    def __init__(self):
        self._name = "Closest"

    def _decide(self, board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        print("us : {}".format(BoardTile.ally_faction))
        our_tiles = board.get_tiles_of_interest()[BoardTile.ally_faction]
        our_tile = our_tiles[0]
        x = our_tile.x
        y = our_tile.y
        nb = our_tile.nb

        human_tiles = board.get_tiles_of_interest()[Faction.HUM]

        min_dist = board.height + board.width
        target_x, target_y = (0,0)
        for tile in human_tiles:
            dist = max(abs(tile.x-our_tile.x), abs(tile.y-our_tile.y))
            if dist < min_dist and tile.nb < nb:
                min_dist = dist
                target_x, target_y = (tile.x, tile.y)

        dir_x = 1 if target_x>our_tile.x else -1 if target_x<our_tile.x else 0
        dir_y = 1 if target_y>our_tile.y else -1 if target_y<our_tile.y else 0
        return [[x,y,nb, our_tile.x+dir_x, our_tile.y+dir_y]]
