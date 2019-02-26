from board_tile import *


class Board():
    def __init__(self,n,m):
        self.__board = np.array([[board_tile(x,y) for y in range(m)] for x in range(n)])
        
    def set_tile(self, tile):
        self.__board[tile.x,tile.y] = tile
    
    def get_tile(self, x, y):
        return self.__board[x, y]
    
    def get_tiles_of_interest(self):
        tiles_of_interest = {Faction.VAMP:[], Faction.WERE:[], Faction.HUM:[]}
        for row in board:
            for tile in row:
                if tile.faction != Faction.EMPT:
                    tiles_of_interest[tile.faction] += [tile]
        return tiles_of_interest[]
    
    def __str__(self):
        s = "\t"
        for j in range(board.shape[0]):
            s+="{}\t".format(j)
        s+="\n"
        for i in range(board.shape[1]):
            s+="{}\t".format(i)
            for j in range(board.shape[0]):
                s+=str(self.__board[i][j])
                s+="\t"
            s+="\n"