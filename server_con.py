from game_client import *
import socket
import struct



class ServerCon():
    def __init__(self, game_client):
        self.__game_client = game_client
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = None
        self.__port = None
        self.__is_connected = False

    def is_connected(self):
        return self.__is_connected

    def connect_to_server(self, addres, port):
        self.__address = addres
        self.__port = port
        self.__socket.connect((self.__address, self.__port))
        self.__is_connected = True

    def _lost_connection(self):
        print("Lost connection with server.")
        self.__is_connected = False

    def _receive_list(self, element_len):
        list_len = self.__socket.recv(1)
        lst = []
        for i in range(list_len):
            element = []
            for j in range(element_len):
                element.append(self.__socket.recv(1))
            if len(element) != element_len:
                self._lost_connection()
            lst.append(element[:])
        if len(lst) != list_len:
            self._lost_connection()
        return lst

    def listen(self):
        message_type = self.__socket.recv(3).decode()
        print("Starting to listen ..")
        if len(message_type) != 3:
            self._lost_connection()
            return False

        if message_type == "SET":
            n = self.__socket.recv(1)
            m = self.__socket.recv(1)
            print("SET: n={}, m={}".format(n, m))
            self.__game_client.callback_set(n, m)

        elif message_type == "HUM":
            lst = self._receive_list(2)
            print("HUM: n={}".format())
            self.__game_client.callback_hum(lst)

        elif message_type == "HME":
            x = self.__socket.recv(1)
            y = self.__socket.recv(1)
            print("HME: x={}, y={}".format(x, y))
            self.__game_client.callback_hme(x, y)

        elif message_type == "MAP":
            lst = self._receive_list(5)
            print("MAP: n={}".format(len(lst), lst))
            self.__game_client.callback_map(lst)

        elif message_type == "UPD":
            lst = self._receive_list(5)
            print("UPD: n={} -> ".format(len(lst), lst))
            self.__game_client.callback_upd(lst)

        elif message_type == "END":
            print("END.")
            self.__game_client.callback_end()

        elif message_type == "BYE":
            print("BYE.")
            self.__game_client.callback_bye()

        else:
            print("Unknown message " + message_type)
        return True



    """ Methodes called by the game client, to send to server """
    def send_nme(self, name):
        paquet = bytes()
        paquet += "NME".encode()
        paquet += bytes(len(name))
        paquet += name.encode()
        self.__socket.send(paquet)

    def send_mov(self, move_list):
        n = len(move_list)
        paquet = bytes()
        paquet += "MOV".encode()
        paquet += bytes(n)
        for move in move_list:
            for i in range(5):
                paquet += bytes(move[i])
        self.__socket.send(paquet)



if __name__ == '__main__':
    print("server_con main starting.")

    sock = ServerCon()
    print("socket created")
    sock.connect_to_server("127.0.0.1", 6666)
    print("socket connected")

    sock.send_name("FOO")
    print("socket connected")

    while(1):
        print("Waiting for message ...")
        print(sock.get_command())
        print("\n")
