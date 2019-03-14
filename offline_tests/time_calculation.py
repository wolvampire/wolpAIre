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
    nb_games = int(sys.argv[1]) if len(sys.argv)>1 else 10
    
    time_panel = np.zeros((5,5))
    depth_panel = np.zeros((5,5))

    for side_board in range(5):
        for n_humans in range(5):
            depth = 2
            max_duration = 0
            while max_duration < 1.7 and depth < 10:
                time_panel[side_board][n_humans] = max_duration
                p2 = GameClient("greed")
                p1 = GameClient("oracle", [1,1,1,1], depth=depth)

                g = GameServer(p1,p2, (n_humans+1)*3, (side_board+1)*2)
                # g.load_game()
                g.new_game()
                #g.print_board()
                
                max_duration = 0
                while(g.nb_games < nb_games):
                    start = time()
                    g.update(1)
                    turn_duration = time() - start
                    max_duration = max(turn_duration,max_duration)
                    g.update(2)
                depth += 1
                print("{} ({}) {} - {} {} ({} {})".format(p2.faction, p2.strat, p2.score, p1.score, p1.faction, p1.strat, p1.depth_max))
            depth_panel[side_board][n_humans] = depth - 2

    print('matrice de profondeur :')
    print(depth_panel)
    print('matrice de temps')
    print(time_panel)