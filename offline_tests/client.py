import random


class GameClient():
    def __init__(self, strat):
        self.score = 0  # nb of games won
        self.decision_fun = 0
        self.strat = strat
        if strat=="greed":
            self.decision_fun = self.greed_move
        elif strat=="random":
            self.decision_fun = self.rand_move
    
    def new_game(self, faction, n, m):
        self.faction = faction
        self.__n = n
        self.__m = m
        
    def decide(self,board):

        # return self.rand_move(board)
        return self.decision_fun(board)
        
        
        
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