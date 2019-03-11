from board_tile import BoardTile
from world_rep import *
from orders_tree import order_node
from decider import *


class GreedyDecider(Decider):
    def __init__(self):
        self._name = "NEED MONNEEEEYYY"

    def _decide(self, board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        Greedy algorithm, simply targets closest 
        """
        # First we get from the board our position and the enemy's and the human's
        our_tiles = self._board.get_tiles_of_interest()[Relation.ALLY]
        our_tile = our_tiles[0]
        x = our_tile.x
        y = our_tile.y
        nb = our_tile.nb
        human_tiles = self._board.get_tiles_of_interest()[Faction.HUM]
        enemy_tiles = self._board.get_tiles_of_interest()[Relation.ENEMY]

        # We look for the closest killable human target
        min_dist = self._board.height + self._board.width
        target_x, target_y = (0,0)
        target_found = False
        for tile in human_tiles:
            dist = BoardTile.distance(tile, our_tile)
            # It needs to be closer and killable
            if dist < min_dist and tile.nb < nb:
                target_found = True
                min_dist = dist
                target_x, target_y = (tile.x, tile.y)

        # If we didnt find an available human tile, we target the enemy
        if not target_found:
            print("GREEDY ALGORITHM : No human target available, engaging the enemy")
            enemy_nb = enemy_tiles[0].nb
            min_dist = BoardTile.distance(our_tile, enemy_tiles[0])
            target_x, target_y = (enemy_tiles[0].x, enemy_tiles[0].y)
            for tile in enemy_tiles:
                dist = BoardTile.distance(our_tile, tile)
                if nb <= enemy_nb:
                    # We need to find a better target
                    if tile.nb < enemy_nb:
                        min_dist = dist
                        enemy_nb = tile.nb
                        target_x, target_y = (tile.x, tile.y)
                else:
                    # We want to find a closer target
                    if dist < min_dist and tile.nb < nb:
                        min_dist = dist
                        enemy_nb = tile.nb
                        target_x, target_y = (tile.x, tile.y)

        print("GREEDY ALGORITHM : Target : {}-{}".format(target_x, target_y))
        # Find out which direction to go to get closer to the target
        dir_x = 1 if target_x>our_tile.x else -1 if target_x<our_tile.x else 0
        dir_y = 1 if target_y>our_tile.y else -1 if target_y<our_tile.y else 0

        return [[x, y, nb, our_tile.x+dir_x, our_tile.y+dir_y]]   
