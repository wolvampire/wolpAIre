import random
from math import ceil

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
    
    def new_game(self, faction, n, m):
        self.faction = faction
        self.__n = n
        self.__m = m
        
    def decide(self,board):

        # return self.rand_move(board)
        return self.decision_fun(board)
        
    
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