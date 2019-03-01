import numpy as np

class order_node():
    id_node=0
    def __init__(self, were_tiles, vamp_tiles, hum_tiles, orders, playing_faction, maximizing_faction, alpha=-np.inf, beta=np.inf, depth=0):
        self.were_tiles = were_tiles
        self.vamp_tiles = vamp_tiles
        self.hum_tiles = hum_tile
        self.orders = orders
        self.maximizing_faction = maximizing_faction
        self.playing_faction = playing_faction
        self.enemy_faction = "VAMP" if playing_faction == "WERE" else "WERE"
        self.alpha = alpha
        self.beta = beta
        self.id_node = order_node.id_node
        self.depth = depth
        order_node.id_node += 1
        
    def compute_all_possibilities(self, ally_tiles, target_tiles):
        """
        for one situation, returns all possible orders (consisting of n troops from a source tile to a target)
        [ one element = one order (a list)
            [ one element = one attribution for an ally tile (a list)
                [], one element = nb of troops for this tile to send to target i
                []
            ],
            [
                [],
                []
            ]
        ]
        """
        if len(ally_tiles) == 1:
            possibilities = []
            orders_for_one_tile = self.compute_orders_for_one_source(ally_tiles[0], target_tiles)
            for order in orders_for_one_tile:
                possibilities.append([order])
            return possibilities
        else:
            ally = ally_tiles[0]
            sub_possibilities = self.compute_all_possibilities(ally_tiles[1:], target_tiles)
            possibilities = []
            for order in self.compute_orders_for_one_tile(ally, target_tiles):
                for poss in sub_possibilities:
                    possibilities.append([order] + poss)
            return possibilities
            


    def create_sons(self):
        return
        
        
def compute_orders_for_one_source(source, ally_tiles, enemy_tiles, human_tiles):
    all_possible_orders = []
    quart_target = [[] for i in range(8)]  # quart_target[i] = list of all targets in quart i
    min_quart = [0 for i in range(8)]
    
    for tile in enemy_tiles:
        q_tile = get_quart_enemy(source, tile)
        quart_target[q_tile] += [tile]
        min_troops = tile.nb//2 + 1
        if min_quart[q_tile] < min_troops:  #  ensures you have more than probability 0.5 of winning the fight
            min_quart[q_tile] = min_troops
    
    for tile in human_tiles:
        q_tile = get_quart_hum(source, tile)
        quart_target[q_tile] += [tile]
        min_troops = tile.nb + 1
        if min_quart[q_tile] < min_troops:
            min_quart[q_tile] = min_troops

    def distribute(nb, bag_id, current_distrib):
        """
        gives all distributions of nb tokens in 8 bags where each bag has either 0 or more than its minimum.
        Returns a possible order distribution and a boolean indicating if it has made a new attribution compared to last distribution.
        This boolean is used to know if the returned distribution is useful or not
        """
        if bag_id==8 or nb==0:
            return [current_distrib], False
        else:
            if min_quart[bag_id] == 0 or min_quart[bag_id] > nb:
                return distribute(nb, bag_id+1, current_distrib)
            else:
                give_distribs = []  # distribs if we choose to give some units to this quarter
                for nb_give in range(min_quart[bag_id], nb+1):
                    give_distrib = [n for n in current_distrib]                    
                    give_distrib[bag_id] = nb_give
                    after_give, allocation_made = distribute(nb-nb_give, bag_id+1, give_distrib)
                    if allocation_made:
                        give_distribs += after_give
                    else : # if we have given too much, the remaining is not enough for the following bags. No need to check the potential distributions.
                        give_distrib = [n for n in current_distrib]                    
                        give_distrib[bag_id] = nb
                        after_give, allocation_made = distribute(0, bag_id+1, give_distrib)
                        give_distribs += after_give
                        break
                
                dont_give, allocation_made = distribute(nb, bag_id+1, current_distrib)
                if allocation_made:
                    return give_distribs + dont_give, len(give_distribs)>0
                    
                return give_distribs, len(give_distribs)>0  # no need to keep the "dont_give" possibility if we don't give to the other bags after that
    
    return distribute(source.nb, 0, [0 for i in range(8)])
    
        
def get_quart_hum(source, target):
    if target.x + target.y <= source.x + source.y - 2:
        return 0
    elif target.x + target.y >= source.x + source.y + 2:
        return 1
    elif target.x < source.x and target.y > source.y and (target.x + target.y >= source.x + source.y - 1) and (target.x + target.y <= source.x + source.y + 1):
        return 2
    elif target.x > source.x and target.y < source.y and (target.x + target.y >= source.x + source.y - 1) and (target.x + target.y <= source.x + source.y + 1):
        return 3
    elif target.x < source.x:
        return 4
    elif target.x > source.x:
        return 5
    elif target.y < source.y:
        return 6
    return 7

        
def get_quart_enemy(source, target):
    if target.x < source.x and target.y < source.y:
        return 0
    elif target.x > source.x and target.y > source.y:
        return 1
    elif target.x < source.x and target.y > source.y:
        return 2
    elif target.x > source.x and target.y < source.y:
        return 3
    elif target.x < source.x and target.y == source.y:
        return 4
    elif target.x > source.x and target.y == source.y:
        return 5
    elif target.x == source.x and target.y < source.y:
        return 6
    return 7
    
        
    
if __name__ == "__main__":
    from board_tile import board_tile
    
    def get_tiles_of_interest(board):
        tiles_of_interest = {"VAMP":[], "WERE":[], "HUM":[]}
        for row in board:
            for tile in row:
                if tile.faction != "EMPT":
                    tiles_of_interest[tile.faction] += [tile]
        return tiles_of_interest
    
    def print_board(board):
        print("\t",end="")
        for j in range(len(board[0])):
            print("{}\t".format(j),end="")
        print()
        for i in range(len(board)):
            print("{}\t".format(i),end="")
            for j in range(len(board[0])):
                print(board[i][j],end="")
                print("\t",end="")
            print("\n")
    
    n = 10
    m = 15

    board = [[board_tile(x,y) for y in range(m)] for x in range(n)]
    board[5][7]=board_tile(5,7,10,"WERE")
    board[3][2]=board_tile(3,2,3,"VAMP")
    board[3][3]=board_tile(3,3,3,"VAMP")
    board[9][9]=board_tile(9,9,9,"HUM")
    board[2][11]=board_tile(2,11,5,"HUM")
        
    source_tile = board[5][7]
    tiles_of_interest = get_tiles_of_interest(board)
    print_board(board)
    pot_orders = compute_orders_for_one_source(source_tile, tiles_of_interest["WERE"], tiles_of_interest["VAMP"], tiles_of_interest["HUM"])
    for pot_order in pot_orders[0]:
        print(pot_order)
        
    print("\t",end="")
    for j in range(m):
        print("{}\t".format(j),end="")
    print()
    for i in range(n):
        print("{}\t".format(i),end="")
        for j in range(m):
            if source_tile != board[i][j]:
                print(get_quart_hum(source_tile,board[i][j]), end="\t")
            else:
                print(board[i][j],end="\t")
        print("\n")
    
    a = input("Return to continue")
        
    print("\t",end="")
    for j in range(m):
        print("{}\t".format(j),end="")
    print()
    for i in range(n):
        print("{}\t".format(i),end="")
        for j in range(m):
            if source_tile != board[i][j]:
                print(get_quart_enemy(source_tile,board[i][j]), end="\t")
            else:
                print(board[i][j],end="\t")
        print("\n")
    
    a = input("Return to continue")
        
        
        
    
        
        
        