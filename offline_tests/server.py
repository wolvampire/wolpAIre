from random import random
from random import randint
from client import GameClient
from time import time
import sys
import os 

from board_tile import board_tile


class GameServer():
    def __init__(self, p1, p2):
        self.__board = [[]]
        self.__n = 0
        self.__m = 0
        self.p1 = p1
        self.p2 = p2
        self.nb_games = 0
        self.nb_tours = 0
        
    def get_board(self):
        return self.__board
    
    def new_game(self, P_hum=0.05):
        self.nb_games += 1
        self.nb_tours = 0
        
        print("New game ! (#{})".format(self.nb_games))
        self.__n = 5
        self.__m = 9

        self.__board = [[board_tile(x,y,randint(1,10),"HUM") if random()<P_hum else board_tile(x,y) for y in range(self.__m)] for x in range(self.__n)]
        
        self.__board[self.__n // 2 - 1][self.__m // 2 - 1]=board_tile(self.__n // 2 - 1,self.__m // 2 - 1,10,"WERE")
        self.__board[self.__n // 2 + 1][self.__m // 2 - 1]=board_tile(self.__n // 2 + 1,self.__m // 2 - 1,10,"VAMP")
        self.p1.new_game("VAMP", self.__n, self.__m)
        self.p2.new_game("WERE", self.__n, self.__m)
        
    def game_report(self):
        if self.p1.max_time > 2 or self.p2.max_time > 2:
            
            print("Length of game : {} turns".format(self.nb_tours))
            print("Max decision time for p1 ({}) : {:.2f}s".format(self.p1.faction, self.p1.max_time))
            print("Max decision time for p2 ({}) : {:.2f}s".format(self.p2.faction, self.p2.max_time))
        
    def print_board(self):
        print("\t",end="")
        for j in range(self.__m):
            print("{}\t".format(j),end="")
        print()
        for i in range(self.__n):
            print("{}\t".format(i),end="")
            for j in range(self.__m):
                print(self.__board[i][j],end="")
                print("\t",end="")
            print("\n")
    

    def update(self, nb):
        self.nb_tours += 1
        
        p = self.p1 if nb==1 else self.p2
        p_enemy = self.p2 if nb==1 else self.p1
            
        p_nb = sum([board_tile.nb for row in self.__board for board_tile in row if board_tile.faction == p.faction])
        p_enemy_nb = sum([board_tile.nb for row in self.__board for board_tile in row if board_tile.faction == p_enemy.faction])
        if p_nb == 0:
            p_enemy.score+=1
            self.game_report()
            self.new_game()
        elif p_enemy_nb == 0:
            p.score+=1
            self.game_report()
            self.new_game() 
        elif self.nb_tours > 100:
            if p_nb > p_enemy_nb:
                p.score += 1
            elif p_nb < p_enemy_nb:
                p_enemy.score += 1
            self.game_report()
            self.new_game()
            
        else:
            moves = p.decide(self.__board)
            faction = p.faction
            enemy = "VAMP" if faction == "WERE" else "WERE"
            for (x,y,nb,xd,yd) in moves:
                if self.__board[x][y].faction == faction and nb <= self.__board[x][y].nb and xd>=x-1 and xd <=x+1 and yd>=y-1 and yd<=y+1 and xd>=0 and xd<self.__n and yd>=0 and yd<self.__m:
                        # print("{} {} from ({},{}) to ({},{})".format(nb, faction,x,y,xd,yd))
                        self.__board[x][y].nb -= nb
                        if self.__board[x][y].nb == 0:
                            self.__board[x][y].faction = "EMPT"
                        result, winner = nb, faction
                        if self.__board[xd][yd].faction == "HUM":
                            result, winner = self.fight_hums(faction, nb, self.__board[xd][yd].nb)
                        elif self.__board[xd][yd].faction == enemy:
                            result, winner = self.fight(faction, enemy, nb, self.__board[xd][yd].nb)
                        elif self.__board[xd][yd].faction == faction:
                            result += self.__board[xd][yd].nb
                        
                        self.__board[xd][yd].nb = result
                        if result != 0:
                            self.__board[xd][yd].faction = winner  
                        else:
                            self.__board[xd][yd].faction = "EMPT"  
                else:
                    print("invalid move : {} {} from ({},{}) to ({},{}). Ignoring.".format(nb, faction,x,y,xd,yd))
    
    def fight_hums(self, faction_att, nb_att, nb_def):
        if nb_att > nb_def:
            return nb_att + nb_def, faction_att
        p = nb_att/(2*nb_def)
        win = random()<p
        if win:
            survivors = 0
            for i in range(nb_att):
                survive = random()<p
                if survive:
                    survivors+=1
            for i in range(nb_def):
                turn = random()<p
                if turn:
                    survivors+=1
            return survivors, faction_att
        else:
            survivors = 0
            for i in range(nb_def):
                survive = random()<(1-p)
                if survive:
                    survivors+=1
            return survivors, "HUM"
            
            
    def fight(self, faction_att, faction_def, nb_att, nb_def):
        p = min(1,max(nb_att/(2*nb_def), nb_att/nb_def-0.5))  # rules in the pdf
        win = random()<p
        if win:
            survivors = 0
            for i in range(nb_att):
                survive = random()<p
                if survive:
                    survivors+=1
            return survivors, faction_att
        else:
            survivors = 0
            for i in range(nb_def):
                survive = random()<(1-p)
                if survive:
                    survivors+=1
            return survivors, faction_def
            
    
if __name__ == "__main__":

    nb_games = int(sys.argv[1]) if len(sys.argv)>1 else 100
    
    p2 = GameClient("greed")
    p1 = GameClient("oracle")

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
    print("{} ({}) {} - {} {} ({})".format(p1.faction, p1.strat, p1.score, p2.score, p2.faction, p2.strat))
    
    
    playing = True
    a = input()
    
    while playing:
        g.update(1)
            
        g.print_board()
        a = input()
        playing = (a != "q")
        
        g.update(2)
        g.print_board()
        a = input()
        playing = (a != "q")
        
        
        
        
        
        
        
        
        
        
        
        
        
        