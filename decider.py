from board import *
from board_tile import *


class Decider():
    def __init__(self):
        self._name = None
        self._board = None

    def get_name(self):
        return self._name

    def decide(self, board):
        '''
        Returns a list of moves, in the shape (x_origin, y_origin, number, x_tar, y_tar)
        '''
        self._board = board
        ret = self._decide(self._board)
        if not self.check_move(ret):
            print("Warning : the move is not valid !")
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
                    move[1] not in range(0, self._board.height) or \
                    move[4] not in range(0, self._board.height):  # Move out of board
                print("Integrity broken : tile out of bounds (board [{}|{}], move : {}).".format(self._board.width,
                                                                                                 self._board.height,
                                                                                                 move))
                rslt = False
                return rslt
        # Rule 2 : We cannot move the enemy
        for move in moves:
            if self._board.tile(move[0], move[1]).relation != Relation.ALLY:
                print("Rule 2 broken : the move {} moves enemy !".format(move))
                rslt = False

        # Rule 3 : Cannot move more than the original pawns
        population_dict = {}
        for move in moves:  # Adding nb of pawns as value per tile (key)
            case = (move[0], move[1])
            population_dict[case] = self._board.tile(move[0], move[1]).nb

        for move in moves:
            case = (move[0], move[1])
            population_dict[case] -= move[2]  # nb of pawns used in the mvt are no more in the tile

        for case, nb_pawns in population_dict.items():
            if nb_pawns < 0:
                print("Rule 3 broken : we move {} pawns more than we should from the tile (coordinates : {}) ".format(
                    -nb_pawns, case))
                rslt = False

        # Rule 4: We can only move to the adjacent tiles
        for move in moves:
            if abs(move[0]-move[3]) > 1 or abs(move[1]-move[4])>1:
                print("Rule 4 broken : in the move {} the pawns don't go to an adjacent tile".format(move))
                rslt = False

        #Rule 5: Source and Target tiles are not the same
        sources_list = []
        for move in moves:
            sources_list.append((move[0], move[1]))

        for move in moves:
            if (move[3], move[4]) in sources_list:
                print("Rule 5 broken : The target {} is already in the sources".format((move[3], move[4])))
                rslt = False

        #Rule 6: We must at least move one pawn
        for move in moves:
            if move[2]<=0:
                print("No pawn is moved in {}".format(move))
                rslt = False

        return rslt
