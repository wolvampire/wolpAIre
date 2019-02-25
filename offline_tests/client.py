import random
from math import ceil, inf
import numpy as np
from board_tile import board_tile

class GameClient():
    def __init__(self, strat):
        self.score = 0  # nb of games won
        self.decision_fun = 0
        self.strat = strat
        if strat=="greed":
            self.decision_fun = self.greed_move
        elif strat=="random":
            self.decision_fun = self.rand_move
        elif strat=="always_attack":
            self.decision_fun = self.always_attack
        elif strat=="oracle":
            self.decision_fun = self.the_oracle
    
    def new_game(self, faction, n, m):
        self.faction = faction
        self.__n = n
        self.__m = m
        
    def decide(self,board):

        # return self.rand_move(board)
        return self.decision_fun(board)
        
    def the_oracle(self,board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """
        our_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == self.faction]
        human_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == "HUM"]
        enemy_tiles = [board_tile for row in board for board_tile in row if board_tile.faction not in ["HUM","EMPT",self.faction]]

        if len(human_tiles) > 0:
            troop_orders, score = self.best_troop_orders(self.faction, our_tiles, enemy_tiles, human_tiles)

            our_mvts = [[order[0],\
                        order[1],\
                        order[2],\
                        order[0] + self.compute_steps(order[0], order[1], order[3], order[4])[0],\
                        order[1] + self.compute_steps(order[0], order[1], order[3], order[4])[1]] for order in troop_orders]
        else : #TODO (strat quand il n'y a plus d'humains)
            pass
        return our_mvts

    def best_troop_orders(self, faction, ally_tiles, enemy_tiles, human_tiles):
        if len(human_tiles) == 0:
            return [], np.sum([tile.nb for tile in ally_tiles + enemy_tiles if tile.faction == self.faction])\
                     - np.sum([tile.nb for tile in ally_tiles + enemy_tiles if tile.faction != self.faction])
        else:
            best_troop_orders = []
            possibilities = self.compute_all_possibilities(ally_tiles, ally_tiles + enemy_tiles + human_tiles)
            score_per_possibility = [-inf]*len(possibilities)
            enemy_possibilities = self.compute_all_possibilities(enemy_tiles, enemy_tiles + ally_tiles + human_tiles)
            for (i,poss) in enumerate(possibilities):
                minmax_score = -inf if faction==self.faction else inf
                for enemy_poss in enemy_possibilities:
                    #next_step_board
                    next_faction, next_ally_tiles, next_enemy_tiles, next_human_tiles = self.compute_next_step_board(poss,\
                                                                                                                     enemy_poss,\
                                                                                                                     faction,\
                                                                                                                     ally_tiles,\
                                                                                                                     enemy_tiles,\
                                                                                                                     human_tiles) 
                    troop_orders, score = self.best_troop_orders(next_faction, next_ally_tiles, next_enemy_tiles, next_human_tiles)
                    if faction == self.faction:
                        if score > minmax_score :
                            minmax_score = score
                    else:
                        if score < minmax_score:
                            minmax_score = score
                score_per_possibility[i] = minmax_score

            best_case_scenario = possibilities[score_per_possibility.index(max(score_per_possibility))]
            for (i,ally) in enumerate(ally_tiles):
                for (j,target) in enumerate(ally_tiles + enemy_tiles + human_tiles):
                    if best_case_scenario[i][j] != 0:
                        best_troop_orders.append([ally.x, ally.y, best_case_scenario[i][j], target.x, target.y])
            return best_troop_orders, max(score_per_possibility)


    def compute_next_step_board(self, poss, enemy_poss, faction, ally_tiles, enemy_tiles, human_tiles):
        turn = faction
        combat_occurred = False
        new_ally_tiles = ally_tiles
        new_enemy_tiles = enemy_tiles
        new_human_tiles = human_tiles
        while not(combat_occurred):
            if turn == faction:
                turn, new_ally_tiles, new_enemy_tiles, new_human_tiles, combat_occurred = \
                    self.sub_func_of_compute_next_step_board(poss, enemy_poss, turn, new_ally_tiles, new_enemy_tiles, new_human_tiles)
            else:
                turn, new_enemy_tiles, new_ally_tiles, new_human_tiles, combat_occurred = \
                    self.sub_func_of_compute_next_step_board(enemy_poss, poss, turn, new_enemy_tiles, new_ally_tiles, new_human_tiles)
        next_faction = "VAMP" if turn=="WERE" else "WERE"
        return next_faction, new_ally_tiles, new_enemy_tiles, new_human_tiles


    def sub_func_of_compute_next_step_board(self, poss, enemy_poss, turn, ally_tiles, enemy_tiles, human_tiles, combat_occurred=False):
        new_ally_tiles = ally_tiles
        new_enemy_tiles = enemy_tiles
        new_human_tiles = human_tiles
        next_faction = "VAMP" if turn=="WERE" else "WERE"
        temporary_new_ally_tiles = []
        for (i, ally) in enumerate(ally_tiles):
            for (j, target) in enumerate(ally_tiles + enemy_tiles + human_tiles):
                print(': {},{}'.format(i,j))
                if poss[i][j] != 0:
                    dir_x, dir_y = self.compute_steps(ally.x, ally.y, target.x, target.y)
                    temporary_new_ally_tiles.append(board_tile(ally.x + dir_x, ally.y + dir_y, nb=poss[i][j], faction=turn))
        new_ally_tiles = temporary_new_ally_tiles
        fusioned_allies = []
        for ally in new_ally_tiles:
            other_new_ally_tiles = new_ally_tiles
            other_new_ally_tiles.remove(ally)
            for other_ally in other_new_ally_tiles:
                if ally.x == other_ally.x and ally.y == other_ally.y and ally not in fusioned_allies and other_ally not in fusioned_allies:
                    temporary_new_ally_tiles.remove(ally)
                    print(2)
                    temporary_new_ally_tiles.remove(other_ally)
                    temporary_new_ally_tiles.append(board_tile(ally.x, ally.y, nb=ally.nb + other_ally.nb, faction=turn))
                    fusioned_allies.append(other_ally)
        new_ally_tiles = temporary_new_ally_tiles
        for ally in temporary_new_ally_tiles:
            for enemy in enemy_tiles:
                if ally.x == enemy.x and ally.y == enemy.y:
                    new_ally_tiles.remove(ally)
                    new_enemy_tiles.remove(enemy)
                    combat_occurred = True
                    if ally.nb >= enemy.nb*1.5:
                        new_ally_tiles.append(board_tile(ally.x, ally.y, nb=ally.nb, faction=turn))
                    else:
                        new_enemy_tiles.append(board_tile(enemy.x, enemy.y, nb=enemy.nb, faction= "WERE" if turn=="VAMP" else "VAMP"))
            for human in human_tiles:
                if ally.x == human.x and ally.y == human.y:
                    new_ally_tiles.remove(ally)
                    new_human_tiles.remove(human)
                    combat_occurred = True
                    if ally.nb > human.nb:
                        new_ally_tiles.append(board_tile(ally.x, ally.y, nb=ally.nb + human.nb, faction=turn))
                    else:
                        new_human_tiles.append(board_tile(human.x, human.y, nb=human.nb, faction="HUM"))
        return next_faction, new_ally_tiles, new_enemy_tiles, new_human_tiles, combat_occurred


    def compute_all_possibilities(self, ally_tiles, target_tiles):
        if len(ally_tiles) == 1:
            possibilities = []
            orders_for_one_tile = self.compute_orders_for_one_tile(ally_tiles[0], target_tiles)  #2
            for order in orders_for_one_tile:
                possibilities.append([order])
            return possibilities
        else:
            ally = ally_tiles[0]
            sub_possibilities = self.compute_all_possibilities(ally_tiles[1:], target_tiles)        #3
            possibilities = []                                                                                  #3
            for order in self.compute_orders_for_one_tile(ally, target_tiles):        #1
                for poss in sub_possibilities:                                                                  #2
                    possibilities.append([order] + poss)
            return possibilities


    def compute_orders_for_one_tile(self, ally, targets):
        enumeration = []
        for k in range(ally.nb//2 if ally.nb%2==0 else ally.nb//2 + 1, ally.nb+1):
            for i in range(len(targets)):
                if k != ally.nb :
                    if k != ally.nb - k:
                        for j in range(len(targets)):
                            if i != j :
                                vector = [0]*len(targets)
                                vector[i] = k
                                vector[j] = ally.nb - k
                                enumeration.append(vector)
                    else:
                        for j in range(i,len(targets)):
                            if i != j :
                                vector = [0]*len(targets)
                                vector[i] = k
                                vector[j] = ally.nb - k
                                enumeration.append(vector)
                else:
                   vector = [0]*len(targets)
                   vector[i] = k
                   enumeration.append(vector)
        return enumeration


    def compute_distance(self, tile1, tile2):
        return max(abs(tile1.x-tile2.x), abs(tile1.y-tile2.y))


    def compute_steps(self, x, y, x_target, y_target):
        dir_x = 1 if x_target > x else -1 if x_target < x else 0
        dir_y = 1 if y_target > y else -1 if y_target < y else 0
        return dir_x, dir_y


    def always_attack(self,board):

        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        """

        our_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == self.faction]
        human_tiles = [board_tile for row in board for board_tile in row if board_tile.faction == "HUM"]
        enemy_tiles = [board_tile for row in board for board_tile in row if board_tile.faction not in ["HUM","EMPT",self.faction]]

        our_mvts = []
        considered_tiles = []
        our_tiles = sorted(our_tiles, \
                    key = lambda tile : min([max(abs(tile.x - other.x), abs(tile.y - other.y)) for other in human_tiles + enemy_tiles]) \
                                            if len(human_tiles + enemy_tiles) > 0 else 0)
        for our_tile in our_tiles:
            #print('vamp en case {},{}'.format(our_tile.x,our_tile.y))
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
                    troops_to_send = self.compute_troops_to_send(our_tile, remaining_troops, target)
                    if troops_to_send > 0 and target not in considered_tiles:
                        #print('ma cible est des {} en {}, {} et j\'envoie {} troupes'.format(target.faction, target.x, target.y, troops_to_send))
                        dir_x = 1 if target.x > our_tile.x else -1 if target.x < our_tile.x else 0
                        dir_y = 1 if target.y > our_tile.y else -1 if target.y < our_tile.y else 0
                        our_mvts.append([our_tile.x, our_tile.y, troops_to_send, our_tile.x + dir_x, our_tile.y + dir_y])
                        remaining_troops -= troops_to_send
                        considered_tiles.append(target)
                        if remaining_troops > 0 and len([ 1 for tile in nearest_targets if tile.nb < remaining_troops]) == 0:
                            our_mvts[-1][2] += remaining_troops
                            remaining_troops = 0
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
                        #print('ma cible est des {} en {}, {}'.format(ally.faction, ally.x, ally.y))
        '''print('Les mouvements des vamps sont :')
        for mvt in our_mvts:
            print('{} vamps font {}, {} --> {},{}'.format(mvt[2],mvt[0],mvt[1],mvt[3],mvt[4]))'''
        return our_mvts

    def compute_troops_to_send(self, our_tile, remaining_troops, target):
        if target.faction == 'HUM':
            if remaining_troops > target.nb:
                return target.nb + 1
            else :
                return 0
        if target.faction not in [our_tile.faction, 'HUM', 'EMPT']:
            if remaining_troops >= target.nb:
                if remaining_troops > ceil(target.nb*1.5):
                    return ceil(target.nb*1.5)
                else:
                    return remaining_troops
            else:
                return 0


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