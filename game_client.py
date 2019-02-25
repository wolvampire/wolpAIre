from server_con import *
from board_tile import *


class GameClient():
    def __init__(self):
        self.__board = [[]]
        self.__connection = ServerCon(self)

    """ Start everything, including connection """
    def start(self, ):
        self.__connection.connect_to_server("127.0.0.1", 6666)
        self.__connection.send_nme("test")
        while self.__connection.is_connected():
            self.__connection.listen()

    """ All callbacks from the server, receiving formated input """
    def callback_set(self, n, m):
        pass

    def callback_hum(self, lst):
        pass

    def callback_hme(self, x, y):
        pass

    def callback_map(self, lst):
        pass

    def callback_upd(self, lst):
        pass

    def callback_end(self):
        pass

    def callback_bye(self):
        pass



if __name__ == '__main__':
    game_client = GameClient()
    game_client.start()
