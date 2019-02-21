from server_con import *
from board_tile import *


class GameClient():
    def __init__(self):
        self.__board = [[]]
        self.__connection = ServerCon(self)

    """ Start everything, including connection """
    def start(self, ):
        
    """ All callbacks from the server, receiving formated input """
    def callback_set(self, n, m):
        

    def callback_hum(self, ):
        

    def callback_hme(self, ):
        

    def callback_map(self, ):
        

    def callback_upd(self, ):
        

    def callback_end(self, ):
        

    def callback_bye(self, ):
        



if __name__ == '__main__':
    game_client = GameClient()
    game_client.start()
