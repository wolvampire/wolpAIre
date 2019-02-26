from board_tile import *


class Board():
    def __init__(self,n,m):
        self.__board = np.array([[board_tile(x,y) for y in range(m)] for x in range(n)])

    
    
    
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