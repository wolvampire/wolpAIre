from board_tile import BoardTile
from world_rep import *
from orders_tree import order_node
from decider import *

class roxxor(Decider):
    def __init__(self):
        self._name = "Xx_D4rK_Sl4y3R_91_xX"
        self._board = [[]]

    def get_name(self):
        return self._name
     
    def decide(self, board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        faction = BoardTile.ally_faction
        enemy_faction = Faction.VAMP if faction==Faction.WERE else Faction.WERE
        
        tiles_of_interest = board.get_tiles_of_interest()
        
        our_tiles = tiles_of_interest[faction]
        enemy_tiles = tiles_of_interest[enemy_faction]
        hum_tiles = tiles_of_interest[Faction.HUM]
        
        all_paths = []
        for source in our_tiles:
            potential_targets = get_potential_targets(source, enemy_tiles, tiles_of_interest[Faction.HUM])
            all_paths += get_all_paths(source, enemy_tiles, potential_targets)
        
        pre_required = {t.id:0 for t in our_tiles}  # at first we don't require any troops from any of our tiles
        
        
        order_tree = order_node([], [], pre_required, all_paths, verbose=False)
        order_tree.create_sons()
        best_gain, best_son = order_tree.get_best_gain()
        
        moves = []
        if best_gain==0:
            for t in our_tiles:
                closest_target = None
                closest_dist = np.inf
                for target in enemy_tiles + hum_tiles:
                    d = dist(t,target)
                    if d<closest_dist:
                        closest_target=target
                        closest_dist=d
                if closest_target is not None:
                    dest_x = t.x+1 if closest_target.x>t.x else t.x-1 if closest_target.x<t.x else t.x
                    dest_y = t.y+1 if closest_target.y>t.y else t.y-1 if closest_target.y<t.y else t.y
                    moves += [(t.x,t.y,t.nb, dest_x, dest_y)]
                                    
        else:
            is_assigned = {t.id:False for t in our_tiles}
            
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
                is_assigned[source_tile.id] = True
                moves += [(x,y,nb, dest_x, dest_y)]
                
                
            for t in our_tiles:
                if not is_assigned[source_tile.id]:
                    closest_ally = None
                    closest_dist = np.inf
                    for ally in our_tiles:
                        if ally != t:
                            d = dist(t,ally)
                            if d<closest_dist:
                                closest_ally=ally
                                closest_dist=d
                    if closest_ally is not None:
                        dest_x = t.x+1 if closest_ally.x>t.x else t.x-1 if closest_ally.x<t.x else t.x
                        dest_y = t.y+1 if closest_ally.y>t.y else t.y-1 if closest_ally.y<t.y else t.y
                        moves += [(t.x,t.y,t.nb, dest_x, dest_y)]
                        if closest_dist == 1:
                            is_assigned[closest_ally.id] = True  # if the targetwasn't already assigned, we don't risk of making them swap places
            
        return moves
