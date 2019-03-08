from board import *
from board_tile import *


class Decider():
    def __init__(self):
        self._name = None
        self._board = [[]]

    def get_name(self):
        return self._name

    def decide(self, board):
        '''
        Returns a list of moves, in the shape (x_origin, y_origin, number, x_tar, y_tar)
        '''
        self._board = board
        ret = self._decide(self._board)
        if not self.check_move(ret):
            print("Warning : he move is not valid !")
        return ret

    def _decide(self, board):
        print("THIS SHOULD NOT BE CALLLED WHAT HAVE YOU DONE")
        '''
        Returns a list of moves, in the shape (x_origin, y_origin, number, x_tar, y_tar)
        '''
        return [[]]

    def check_move(self, moves):
        rslt = True
        # Rule 1 : At least one move is
        if len(moves) == 0:
            print("Rule 1 broken : There is no move.")
            rlst = False
        # Check message integrity
        for move in moves:
            if len(move) != 5:
                print("Integrity broken : A move has  length of {} instead of 5 (move : {}).".format(len(move), move))
                rslt = False
                return rslt
            if move[0] not in range(0, self._board.width) or \
                    move[3] not in range(0, self._board.width) or \
                    move[2] not in range(0, self._board.height) or \
                    move[4] not in range(0, self._board.height): # Move out of borad
                print("Integrity broken : tile out of bounds (board [{}|{}], move : {}).".format(self._board.width,
                                                                                                 self._board.height,
                                                                                                 move))
                rslt = False
                return rslt
        # Rule 2 : We cannot move the enemy
        for move in moves:
            if self._board(move[0], move[1]).relation != Relation.ALLY :
                print("Rule 2 broken : the move {} moves enemy !".format(move))
                rslt = False

        # Rule 3 :
        return rslt
