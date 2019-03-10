from random import random
from random import randint
from client import GameClient
from server import GameServer
from time import time
import sys
import os 
import numpy as np

from board_tile import board_tile

if __name__ == '__main__':
    nb_games = int(sys.argv[1]) if len(sys.argv)>1 else 1000
    
    coefs_panel = np.zeros((4,4,4,4))
    for i in range(4):
        for j in range(4):
            for k in range(4):
                for l in range(4):
                    if [i,j,k,l] == [0,0,0,0]:
                        coefs_panel[i][j][k][l] = 0
                    else:
                        coefs = [i,j,k,l]

                        p2 = GameClient("greed")
                        p1 = GameClient("oracle", coefs)

                        g = GameServer(p1,p2)
                        # g.load_game()
                        g.new_game()
                        g.print_board()
                        
                        s = time()
                        
                        while(g.nb_games < nb_games):
                            g.update(1)
                            
                            g.update(2)
                            if time()-s >= 1:
                                # g.print_board()
                                s = time()
                        print("{} ({}) {} - {} {} ({} {})".format(p2.faction, p2.strat, p2.score, p1.score, p1.faction, p1.strat, p1.coefs))
                        coefs_panel[i][j][k][l] = (p1.score / nb_games)*100
    print(coefs_panel)
    print('best score for coefs : {}'.format(np.unravel_index(coefs_panel.argmax(), coefs_panel.shape)))