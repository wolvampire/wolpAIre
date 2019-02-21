from game_client import *
import socket
import struct



class ServerCon():
    def __init__(self, game_client):
        self.__game_client = game_client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = None
        self.port = None

    def connect_to_server(self, addres, port):
        self.socket.connect((addres, port))

    def send_name(self, name):
        paquet = bytes()
        paquet += "NME".encode()
        paquet += bytes(len(name))
        paquet += name.encode()
        self.socket.send(paquet)

    def get_command(self):
        commande = bytes()
        while len(commande)<3:
            commande += self.socket.recv(3-len(commande))
        return commande.decode()

    """ Methodes called by the game client, to send to server """
    def send_nme(self, ):
        

    def send_mov(self, ):
        



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
