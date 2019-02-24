import random
from world_rep import get_all_paths, get_potential_targets, get_tiles_of_interest, dist
from orders_tree import order_node
from time import time
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
            self.decision_fun = self.roxxor_move_verbose
            
            
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
        
        
        
    def greed_move(self,board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == self.faction]
        our_tile = our_tiles[0]
        x = our_tile.x
        y = our_tile.y
        nb = our_tile.nb
        
        human_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == "HUM"]
        
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
        
        order_tree = order_node([], [], pre_required, all_paths)
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
        all_paths = []
        for source in our_tiles:
            potential_targets = get_potential_targets(source, enemy_tiles, tiles_of_interest["HUM"])
            all_paths += get_all_paths(source, enemy_tiles, potential_targets)
        
        pre_required = {t.id:0 for t in our_tiles}  # at first we don't require any troops from any of our tiles
        
        
        order_tree = order_node([], [], pre_required, all_paths)
        order_tree.create_sons()
        best_gain, best_son = order_tree.get_best_gain()
        

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
        return moves