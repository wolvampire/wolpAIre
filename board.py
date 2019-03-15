import numpy as np
from board_tile import *


class Board():
    def __init__(self, n, m):
        self.__width = n
        self.__height = m
        self.__board = np.array([[BoardTile(x,y) for y in range(m)] for x in range(n)])

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def tile(self, x, y):
        return self.__board[x, y]

    def get_tiles_of_interest(self):
        tiles_of_interest = {
            Faction.VAMP:[],
            Faction.WERE:[],
            Faction.HUM:[],
            Relation.ALLY:[],
            Relation.ENEMY:[],
            Relation.HUM:[]
        }
        for row in self.__board:
            for tile in row:
                if tile.faction != Faction.EMPT:
                    tiles_of_interest[tile.faction] += [tile.copy()]
                    tiles_of_interest[tile.relation] += [tile.copy()]
        return tiles_of_interest

    def __str__(self):
        s = "\t"
        for j in range(self.__board.shape[0]):
            s+="{}\t".format(j)
        s+="\n\n"
        for i in range(self.__board.shape[1]):
            s+="{}\t".format(i)
            for j in range(self.__board.shape[0]):
                s+=str(self.__board[j][i])
                s+="\t"
            s+="\n\n"
        return s
