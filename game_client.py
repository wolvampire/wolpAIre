from server_con import *
from board_tile import *


class GameClient():
    def __init__(self):
        self.__board, self.__connection, self.__startingHome = initialize(self)

    def start(self, ):
                                                        #TODO

    def callback_set(self, n, m):
        self.__board = [[0]*m]*n
        return True

    def callback_hum(self, nHouses, housesCoordinates):
        if nHouses == len(housesCoordinates):
            for (x,y) in housesCoordinates:
                self.__board[x][y] = "House"            #TODO : Instancier board_tile
        else:
            return False
        return True

    def callback_hme(self, x, y):
        self.__board[x][y] = "Nous"                     #TODO : Instancier board_tile // Peut etre pas besoin
        self.__startingHome = [x,y]
        return True

    def callback_upd(self, nChanges, changesInfosList):
        update_map(self, nChanges, changesInfosList)

    def callback_map(self, nTiles, tilesInfosList):
        update_map(self, nTiles, tilesInfosList)

    def callback_end(self):
        self.__board, self.__connection, self.__startingHome = initialize(self)

    def callback_bye(self):
                                                        #TODO


    def initialize(self):
        return [[]], ServerCon(self), []

    def update_map(self, nChanges, changesInfosList):
        if nChanges == len(changesInfosList):
            for change in changesInfosList:
                x = change[0]
                y = change[1]
                nHuman = change[2]
                nVamp = change[3]
                nWerew = change[4]
                if (nHuman*nVamp == 0) and (nHuman*nWerew == 0) and (nVamp*nVamp == 0):
                    self.__board[x][y] = "tile avec les humanoides"             #TODO : Tiles
                else :
                    return False
        else:
            return False
        return True


if __name__ == '__main__':
    game_client = GameClient()
    game_client.start()
