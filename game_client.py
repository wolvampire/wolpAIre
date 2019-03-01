from server_con import *
from board_tile import *
from decider import *

    
class GameClient():
    def __init__(self):
        self.__decider = Decider()

    def start_connection(self):
        self.__connection = ServerCon(self)
        self.__connection.connect_to_server("127.0.0.1", 6666)
        self.__connection.send_nme("test")
        while self.__connection.is_connected():
            self.__connection.listen()
        
    def start(self):
        '''
        reset for a new game
        '''
        self.__board = [[]]
        self.__n = 0
        self.__m = 0
        self.__startingHome = []
        self.__us = None  # equals "VAMP" or "WERE"

    def give_decider(self, decider):
        self.__decider = decider

    def callback_set(self, n, m):
        '''
        All callbacks from the server, receiving formated input
        '''
        self.start()
        self.__board = [[board_tile(x,y) for y in range(n)] for x in range(m)]
        print(self.__board)
        return True

    def callback_hum(self, housesCoordinates):
        for (x,y) in housesCoordinates:
            print("x : {}; y : {}".format(x, y))
            self.__board[x][y] = board_tile(x,y,faction=Faction.HUM)
        return True

    def callback_hme(self, x, y):
        self.__startingHome = [x,y]
        return True

    def callback_upd(self, changesInfosList):
        update_success =  self.update_map(changesInfosList)
        if update_success:
            moves = self._decide()
            self.__connection.send_mov(moves)
        return update_success

    def callback_map(self, tilesInfosList):
        return_value = self.update_map(tilesInfosList)
        if self.__board[self.__startingHome[0]][self.__startingHome[1]].faction in [Faction.VAMP,Faction.WERE]:
            self.__us = self.__board[self.__startingHome[0]][self.__startingHome[1]].faction
        else:
            print("Error callback_map : home faction is {}".format(self.__board[self.__startingHome[0]][self.__startingHome[1]].faction))
            return False
        return return_value

    def callback_end(self):
        self.start()

    def callback_bye(self):
        pass
        #TODO @paternose

    def update_map(self, changesInfosList):
        for change in changesInfosList:
            x = change[0]
            y = change[1]
            nHum = change[2]
            nVamp = change[3]
            nWere = change[4]
            if (nHum*nVamp == 0) and (nHum*nWere == 0) and (nVamp*nWere == 0):
                #  checks that there is no couple of faction on a single tile
                if nHum != 0:
                    self.__board[x][y] = board_tile(x,y,nb=nHum,faction=Faction.HUM)
                if nVamp != 0:
                    self.__board[x][y] = board_tile(x,y,nb=nVamp,faction=Faction.VAMP)
                if nWere != 0:
                    self.__board[x][y] = board_tile(x,y,nb=nWere,faction=Faction.WERE)
            else :
                return False
        return True        
        
    def _decide(self):
        return self.__decider.decide(self.__board)
        

if __name__ == '__main__':
    import closest
    game_client = GameClient()
    game_client.give_decider(closest.ClosestDecider())
    game_client.start_connection()
