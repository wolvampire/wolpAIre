import random
from world_rep import get_all_paths, get_potential_targets, get_tiles_of_interest, dist
from orders_tree import order_node
from time import time
from math import ceil
import numpy as np

class GameClient():
    def __init__(self, strat):
        self.score = 0  # nb of games won
        self.decision_fun = 0
        self.strat = strat
        if strat=="greed":
            self.decision_fun = self.greed_move
        elif strat=="random":
            self.decision_fun = self.rand_move
        elif strat=="roxxor":
            self.decision_fun = self.roxxor_move#_verbose
        elif strat=="roxxor_v":
            self.decision_fun = self.roxxor_move_verbose
        elif strat=="always_attack":
            self.decision_fun = self.always_attack
    
    def new_game(self, faction, n, m):
        self.faction = faction
        self.__n = n
        self.__m = m
        self.max_time=0
        
    def decide(self,board):
        s = time()
        moves = self.decision_fun(board)
        t = time()-s
        if t>self.max_time:
            self.max_time=t
        return moves
        
    
    def always_attack(self,board):

        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """

        our_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == self.faction]
        human_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == "HUM"]
        enemy_tiles = [board_tile for row in board for board_tile in row if board_tile.faction not in ["HUM","EMPT",self.faction]]

        our_mvts = []
        considered_tiles = []
        for our_tile in our_tiles:
            print('loups en case {}, {}'.format(our_tile.x,our_tile.y))
            nb = our_tile.nb
            targets = []

            for tile in human_tiles + enemy_tiles:
                if nb > tile.nb:
                    targets.append(tile)

            if len(targets) > 0:
                nearest_targets = sorted(targets, key = lambda tile : max(abs(tile.x - our_tile.x), abs(tile.y - our_tile.y)))
                remaining_troops = nb
                while remaining_troops > 0 and len(nearest_targets) > 0:
                    target = nearest_targets[0]
                    nearest_targets = nearest_targets[1:]
                    if remaining_troops > target.nb and target not in considered_tiles:
                        print('ma cible est des {} en {}, {}'.format(target.faction, target.x, target.y))
                        dir_x = 1 if target.x > our_tile.x else -1 if target.x < our_tile.x else 0
                        dir_y = 1 if target.y > our_tile.y else -1 if target.y < our_tile.y else 0
                        troops_to_send = target.nb + 1 if target.faction == "HUM" else \
                                         min(ceil(target.nb*1.5), remaining_troops)
                        our_mvts.append([our_tile.x, our_tile.y, target.nb + 1, our_tile.x + dir_x, our_tile.y + dir_y])
                        remaining_troops -= target.nb + 1
                        considered_tiles.append(target)
            else:
                nearest_allies = sorted(our_tiles, key = lambda tile : max(abs(tile.x - our_tile.x), abs(tile.y - our_tile.y)))
                nearest_allies = nearest_allies[1:]
                ally_found = False
                while not(ally_found) and len(nearest_allies) > 0 :
                    ally = nearest_allies[0]
                    nearest_allies = nearest_allies[1:]
                    if ally.nb > nb :
                        dir_x = 1 if ally.x > our_tile.x else -1 if ally.x < our_tile.x else 0
                        dir_y = 1 if ally.y > our_tile.y else -1 if ally.y < our_tile.y else 0
                        our_mvts.append([our_tile.x, our_tile.y, nb, our_tile.x + dir_x, our_tile.y + dir_y])
                        ally_found = True
                        print('ma cible est des {} en {}, {}'.format(ally.faction, ally.x, ally.y))
        return our_mvts


    def greed_move(self,board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == self.faction]
        our_tile = our_tiles[0]
        x = our_tile.x
        y = our_tile.y
        nb = our_tile.nb
        enemy_faction = "VAMP" if self.faction=="WERE" else "WERE"
        human_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == "HUM"]
        enemy_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == enemy_faction]
        
        min_dist = self.__n + self.__m
        target_x, target_y = (0,0)
        for tile in human_tiles:
            dist = max(abs(tile.x-our_tile.x), abs(tile.y-our_tile.y))
            if dist < min_dist and tile.nb < nb:
                min_dist = dist
                target_x, target_y = (tile.x, tile.y)
                
        if len(human_tiles)==0:
            for tile in enemy_tiles:
                dist = max(abs(tile.x-our_tile.x), abs(tile.y-our_tile.y))
                if dist < min_dist and tile.nb < nb:
                    min_dist = dist
                    target_x, target_y = (tile.x, tile.y)
            
            
        dir_x = 1 if target_x>our_tile.x else -1 if target_x<our_tile.x else 0
        dir_y = 1 if target_y>our_tile.y else -1 if target_y<our_tile.y else 0
        
        return [[x,y,nb, our_tile.x+dir_x, our_tile.y+dir_y]]    
        
    def rand_move(self,board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = [board_tile for row in board for board_tile in row
                             if board_tile.faction == self.faction]
        for tile in our_tiles:
            if tile.nb==0:
                print("abberation :",tile.x,tile.y)
        
        random_tile = random.choice(our_tiles)  # awesome IA algorithm
        x = random_tile.x
        y = random_tile.y
        n = random_tile.nb
        
        pot_dest = [(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
        pot_dest_filtered = [(i,j) for (i,j) in pot_dest if i>=0 and i<self.__n and j >=0 and j<self.__m]
        
        dest_x, dest_y = random.choice(pot_dest_filtered)

        random_n = random.choice(list(range(1,n+1)))

        return [[x,y,random_n, dest_x, dest_y]]
        
        
    def roxxor_move_verbose(self,board):
        enemy_faction = "VAMP" if self.faction=="WERE" else "WERE"
        tiles_of_interest = get_tiles_of_interest(board)
        our_tiles = tiles_of_interest[self.faction]
        enemy_tiles = tiles_of_interest[enemy_faction]
        print("potential targets for {}".format(self.faction))        
        all_paths = []
        for source in our_tiles:
            potential_targets = get_potential_targets(source, enemy_tiles, tiles_of_interest["HUM"])
            all_paths += get_all_paths(source, enemy_tiles, potential_targets)

            for tile in potential_targets:
                print("({},{} - {}) -> ({},{} - {} - {}t)".format(source.x, source.y, source, tile.x, tile.y, tile, dist(source, tile)))
            
        print("potential paths for {}".format(self.faction))
        
        for path in all_paths:
            print(path)
        
        
        pre_required = {t.id:0 for t in our_tiles}  # at first we don't require any troops from any of our tiles
        
        print("Creating decision tree...")
        
        order_tree = order_node([], [], pre_required, all_paths, verbose=True)
        order_tree.create_sons()
        best_gain, best_son = order_tree.get_best_gain()
        
        print("best solution found :")
        print(best_son)
        
        if best_gain==0:
            return self.greed_move(board)       
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
        print(moves)            
        return moves
    
    
        
    def roxxor_move(self,board):
        enemy_faction = "VAMP" if self.faction=="WERE" else "WERE"
        tiles_of_interest = get_tiles_of_interest(board)
        our_tiles = tiles_of_interest[self.faction]
        enemy_tiles = tiles_of_interest[enemy_faction]
        hum_tiles = tiles_of_interest["HUM"]
        all_paths = []
        for source in our_tiles:
            potential_targets = get_potential_targets(source, enemy_tiles, hum_tiles)
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