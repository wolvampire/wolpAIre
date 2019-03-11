from board_tile import BoardTile
from math import inf
from decider import *


class OracleDecider(Decider):
    def __init__(self):
        self._name = "THE ORACLE"
        self.coefs = [1, 1, 1, 1]
        self.depth_max = 10 # max depth when exploring the tree of possibilities
        

    def _decide(self, board):
        """
        returns a list of (x,y,n,x',y'), stating that we want to move n units form tile (x,y) to (x',y')
        This strategy relies on a simplified approach of the game. We consider that every ally tile can target one or
        several targets depending on how many troops the tile has, the targets being the ally, the enemy and human tiles.
        We first call best_troop_orders with the information about the actual board situation. 
        Once all the targetting possibilities are computed for the ally and the enemy, we simulate the next turns until
        two units collide. We then call the recursive function best_troop_orders giving it the information about
        the simulated board for the current targetting possibility. The recursive search goes on until a final node 
        (i.e. win, loss, no more humans or maximum depth of search reached), returning the heuristic of the foreseen board.
        Then, with the returned values, the alpha-beta algoriths helps reducing the number of possibilities to explore.
        """
        our_tiles = board.get_tiles_of_interest()[Relation.ALLY]
        enemy_tiles = board.get_tiles_of_interest()[Relation.ENEMY]
        human_tiles = board.get_tiles_of_interest()[Faction.HUM]
        
        print('Je suis {}'.format(BoardTile.ally_faction))
        if len(our_tiles) == 0:
            return []

        #strategy if there are some humans
        if len(human_tiles) > 0:
            troop_orders, score = self.best_troop_orders(BoardTile.ally_faction, our_tiles, enemy_tiles, human_tiles)
            print("Troop orders ({}) : {}".format(troop_orders, score))
            our_mvts = [[order[0],\
                        order[1],\
                        order[2],\
                        order[0] + self.compute_steps(order[0], order[1], order[3], order[4])[0],\
                        order[1] + self.compute_steps(order[0], order[1], order[3], order[4])[1]] for order in troop_orders]
            return our_mvts
        #simple strategy if there are no humans left
        else:
            print("Troop orders : no human !")
            our_mvts = []
            if len(our_tiles) > 1:
                our_tiles = sorted(our_tiles, key = lambda tile : tile.nb, reverse=True)
                biggest_ally = our_tiles[0]
                for ally in our_tiles[1:]:
                    dir_x, dir_y = self.compute_steps(ally.x, ally.y, biggest_ally.x, biggest_ally.y)
                    our_mvts.append([ally.x, ally.y, ally.nb, ally.x + dir_x, ally.y + dir_y])
                return our_mvts
            else:
                enemy_tiles = sorted(enemy_tiles, key = lambda tile : tile.nb)
                smallest_enemy = enemy_tiles[0]
                ally = our_tiles[0]
                dir_x, dir_y = self.compute_steps(ally.x, ally.y, smallest_enemy.x, smallest_enemy.y)
                our_mvts.append([ally.x, ally.y, ally.nb, ally.x + dir_x, ally.y + dir_y])
                return our_mvts

    def best_troop_orders(self, faction, ally_tiles, enemy_tiles, human_tiles, layer=1, alpha=-inf, beta=inf, return_troop_orders=True,\
                            previous_ally_tiles=None, previous_enemy_tiles=None):
        '''
        Recursive fonction that implements the tree-search and the alpha-beta optimization
        '''
        layer += 1
        best_troop_orders = []
        #terminal case
        if len(human_tiles) == 0 or len(ally_tiles) == 0 or len(enemy_tiles) == 0 or layer-1 >= self.depth_max:
            heuristic = self.heuristic4(ally_tiles, enemy_tiles, human_tiles, faction, previous_ally_tiles, previous_enemy_tiles) if faction==BoardTile.ally_faction\
                         else self.heuristic4(enemy_tiles, ally_tiles, human_tiles, faction, previous_enemy_tiles, previous_ally_tiles)
            if return_troop_orders:
                return best_troop_orders, heuristic
            else:
                return heuristic
        else:
            #computing the different targetting possibilities for the ally and the enemy
            possibilities = self.compute_all_possibilities(ally_tiles, ally_tiles + enemy_tiles + human_tiles, seperation_per_troop=1)
            enemy_possibilities = self.compute_all_possibilities(enemy_tiles, enemy_tiles + ally_tiles + human_tiles, seperation_per_troop=1)
            #initializing the list of score for the possibilities and the node value for the alpha-beta optimization
            score_per_possibility = [-inf if faction==BoardTile.ally_faction else inf]*len(possibilities)
            ally_node_value = -inf if faction==BoardTile.ally_faction else inf
            for (i,poss) in enumerate(possibilities):
                #Since we loop among the enemy possibilities for each ally possibility, we have to adapt the alpha-beta algorithm
                #so that the values for the minimizer and maximizer nodes do not mix up. Thus the sub_alpha and sub_beta.
                #They are inizialized to alpha and beta
                sub_alpha = alpha
                sub_beta = beta
                #The score to minimize (maximize) is initialized to infinity if the function is called on the ally's turn
                #(-infinity for the enemy's turn)
                #Note that this initialization is for the inner loop below : the enemy will want to minimize the score
                minmax_score = inf if faction==BoardTile.ally_faction else -inf
                enemy_node_value = inf if faction==BoardTile.ally_faction else -inf
                #checks the usefulness of a possibility so that the algorithm doesn't look for useless subtrees
                poss_is_interesting = self.check_interesting_possibility(poss, ally_tiles, enemy_tiles, human_tiles)
                all_troop_static = len([1 for l in range(len(poss)) if poss[l][l] == ally_tiles[l].nb]) == len(ally_tiles)
                if all_troop_static or not(poss_is_interesting) :
                    score_per_possibility[i] = -inf if faction==BoardTile.ally_faction else inf
                else:
                    for (j,enemy_poss) in enumerate(enemy_possibilities):
                        #Given the targets for each ally and enemy, the function below computes the future turns until
                        #two or more tiles interact. It returns the resulting board situation.
                        next_faction, next_ally_tiles, next_enemy_tiles, next_human_tiles = self.compute_next_state_board(poss,\
                                                                                                                          enemy_poss,\
                                                                                                                          faction,\
                                                                                                                          ally_tiles,\
                                                                                                                          enemy_tiles,\
                                                                                                                          human_tiles)
                        #Depending on who is to play next, we call the recursive function with the correct arguments.
                        if next_faction == faction:
                            score = self.best_troop_orders(next_faction,\
                                                           next_ally_tiles,\
                                                           next_enemy_tiles,\
                                                           next_human_tiles,\
                                                           previous_ally_tiles = ally_tiles,\
                                                           previous_enemy_tiles = enemy_tiles,\
                                                           layer=layer,\
                                                           alpha=sub_alpha,\
                                                           beta=sub_beta,\
                                                           return_troop_orders=False)
                        else :
                            score = self.best_troop_orders(next_faction,\
                                                           next_enemy_tiles,\
                                                           next_ally_tiles,\
                                                           next_human_tiles,\
                                                           previous_ally_tiles = enemy_tiles,\
                                                           previous_enemy_tiles = ally_tiles,\
                                                           layer=layer,\
                                                           alpha=sub_alpha,\
                                                           beta=sub_beta,\
                                                           return_troop_orders=False)
                        #In the inner loop, the score is minimized if the function has been called on the ally's turn because
                        #we are looping through the enemy's possibilities. It is maximized otherwise for the symetrical reason.
                        if faction == BoardTile.ally_faction:
                            minmax_score = min(score,minmax_score)
                            '''if layer == 2:
                                print('minimax {} when score {} for poss {} and enemy poss {}'.format(minmax_score, score, i, j))'''
                            enemy_node_value = min(enemy_node_value, score)
                            sub_beta = min(sub_beta,enemy_node_value)
                        else:
                            minmax_score = max(score,minmax_score)
                            enemy_node_value = max(enemy_node_value, score)
                            sub_alpha = max(sub_alpha,enemy_node_value)
                        #alpha-beta pruning
                        if sub_alpha >= sub_beta:
                            break
                    #In the outer loop, the score is maximized if the function has been called on the ally's turn because
                    #we are looping through the ally's possibilities. It is maximized otherwise for the symetrical reason.
                    score_per_possibility[i] = minmax_score
                    if faction == BoardTile.ally_faction:
                        ally_node_value = max(ally_node_value, minmax_score)
                        alpha = max(alpha, ally_node_value)
                    else:
                        ally_node_value = min(ally_node_value, minmax_score)
                        beta = min(beta, ally_node_value)
                    #alpha-beta pruning
                    if alpha >= beta:
                        break
            if not(return_troop_orders):
                return max(score_per_possibility) if faction == BoardTile.ally_faction else min(score_per_possibility)
            else:
                #This is executed only for the initial call of the function
                #The best case scenario is the possibility with the highest score
                best_case_scenario = possibilities[score_per_possibility.index(max(score_per_possibility))]
                #Compute troop order from best case scenario
                for (i,ally) in enumerate(ally_tiles):
                    for (j,target) in enumerate(ally_tiles + enemy_tiles + human_tiles):
                        if best_case_scenario[i][j] != 0:
                            best_troop_orders.append([ally.x, ally.y, best_case_scenario[i][j], target.x, target.y])
                print("Possibilities {}\nScores : {}".format(possibilities,score_per_possibility))
                return best_troop_orders, (max(score_per_possibility) if faction == BoardTile.ally_faction else min(score_per_possibility))


    def compute_next_state_board(self, poss, enemy_poss, faction, ally_tiles, enemy_tiles, human_tiles):
        turn = faction
        conflict_occured = False
        new_ally_tiles = ally_tiles[:]
        new_enemy_tiles = enemy_tiles[:]
        new_human_tiles = human_tiles[:]
        splits_per_ally = list(np.count_nonzero(poss, axis=1))
        splits_per_enemy = list(np.count_nonzero(enemy_poss, axis=1))
        if splits_per_ally != list(np.ones((len(ally_tiles),), dtype=int)) and faction==BoardTile.ally_faction: #check split
            for (i,ally) in enumerate(ally_tiles):
                new_ally_tiles.remove(ally)
                for (j,target) in enumerate(ally_tiles + enemy_tiles + human_tiles):
                    if poss[i][j] != 0:
                        dir_x, dir_y = self.compute_steps(ally.x, ally.y, target.x, target.y)
                        new_ally_tiles.append(BoardTile(ally.x + dir_x, ally.y + dir_y, nb=poss[i][j], faction=faction))
            new_ally_tiles, new_enemy_tiles, new_human_tiles, conflict_occured = self.check_conflict_and_compute_battle(new_ally_tiles,\
                                                                                                                       new_enemy_tiles,\
                                                                                                                       new_human_tiles,\
                                                                                                                       len(ally_tiles),\
                                                                                                                       faction,\
                                                                                                                       conflict_occured)
        elif splits_per_enemy != list(np.ones((len(enemy_tiles),), dtype=int)) and faction!=BoardTile.ally_faction:
            for (i,enemy) in enumerate(enemy_tiles):
                new_enemy_tiles.remove(enemy)
                for (j,target) in enumerate(enemy_tiles + ally_tiles + human_tiles):
                    if enemy_poss[i][j] != 0:
                        dir_x, dir_y = self.compute_steps(enemy.x, enemy.y, target.x, target.y)
                        new_enemy_tiles.append(BoardTile(enemy.x + dir_x, enemy.y + dir_y, nb=enemy_poss[i][j], faction=faction))
            new_enemy_tiles, new_ally_tiles, new_human_tiles, conflict_occured = self.check_conflict_and_compute_battle(new_enemy_tiles,\
                                                                                                                       new_ally_tiles,\
                                                                                                                       new_human_tiles,\
                                                                                                                       len(enemy_tiles),\
                                                                                                                       faction,\
                                                                                                                       conflict_occured)
        else:
            while not(conflict_occured):
                if turn == faction:
                    turn, new_ally_tiles, new_enemy_tiles, new_human_tiles, conflict_occured = \
                        self.steps_until_new_state(poss, turn, new_ally_tiles, new_enemy_tiles, new_human_tiles)
                else:
                    turn, new_enemy_tiles, new_ally_tiles, new_human_tiles, conflict_occured = \
                        self.steps_until_new_state(enemy_poss, turn, new_enemy_tiles, new_ally_tiles, new_human_tiles)
        next_faction = Faction.VAMP if turn==Faction.WERE else Faction.WERE
        return next_faction, new_ally_tiles, new_enemy_tiles, new_human_tiles


    def steps_until_new_state(self, poss, turn, ally_tiles, enemy_tiles, human_tiles, conflict_occured=False):
        next_turn = Faction.VAMP if turn==Faction.WERE else Faction.WERE
        temporary_new_ally_tiles = []
        for (i, ally) in enumerate(ally_tiles):
            for (j, target) in enumerate(ally_tiles + enemy_tiles + human_tiles):
                if poss[i][j] != 0:
                    dir_x, dir_y = self.compute_steps(ally.x, ally.y, target.x, target.y)
                    temporary_new_ally_tiles.append(BoardTile(ally.x + dir_x, ally.y + dir_y, nb=poss[i][j], faction=turn))
        new_ally_tiles, new_enemy_tiles, new_human_tiles, conflict_occured = self.check_conflict_and_compute_battle(temporary_new_ally_tiles,\
                                                                                                                   enemy_tiles,\
                                                                                                                   human_tiles,\
                                                                                                                   len(ally_tiles),\
                                                                                                                   turn,\
                                                                                                                   conflict_occured)
        return next_turn, new_ally_tiles, new_enemy_tiles, new_human_tiles, conflict_occured


    def check_conflict_and_compute_battle(self, temporary_new_ally_tiles, enemy_tiles, human_tiles, n_allies_previous_turn, turn, conflict_occured):
        new_enemy_tiles = enemy_tiles[:]
        new_human_tiles = human_tiles[:]
        new_ally_tiles = temporary_new_ally_tiles[:]
        fusioned_allies = []
        fusioned_allies_dict = {}
        for ally in new_ally_tiles:
            try:
                fusioned_allies_dict['{};{}'.format(ally.x,ally.y)] += ally.nb
            except:
                fusioned_allies_dict['{};{}'.format(ally.x,ally.y)] = ally.nb
        temporary_new_ally_tiles = []
        for key in fusioned_allies_dict.keys():
            temporary_new_ally_tiles.append(BoardTile(int(key.split(';')[0]), int(key.split(';')[1]), nb=fusioned_allies_dict[key], faction=turn))
        if len(temporary_new_ally_tiles) < len(new_ally_tiles):
            conflict_occured = True
        if len(new_ally_tiles) != n_allies_previous_turn:
            conflict_occured = True
        new_ally_tiles = temporary_new_ally_tiles[:]
        for ally in temporary_new_ally_tiles:
            for enemy in enemy_tiles:
                if ally.x == enemy.x and ally.y == enemy.y:
                    new_ally_tiles.remove(ally)
                    new_enemy_tiles.remove(enemy)
                    conflict_occured = True
                    if ally.nb >= enemy.nb*1.5:
                        new_ally_tiles.append(BoardTile(ally.x, ally.y, nb=ally.nb, faction=turn))
                    else:
                        new_enemy_tiles.append(BoardTile(enemy.x, enemy.y, nb=enemy.nb, faction= Faction.WERE if turn==Faction.VAMP else Faction.VAMP))
            for human in human_tiles:
                if ally.x == human.x and ally.y == human.y:
                    new_ally_tiles.remove(ally)
                    new_human_tiles.remove(human)
                    conflict_occured = True
                    if ally.nb > human.nb:
                        new_ally_tiles.append(BoardTile(ally.x, ally.y, nb=ally.nb + human.nb, faction=turn))
                    else:
                        new_human_tiles.append(BoardTile(human.x, human.y, nb=human.nb, faction=Faction.HUM))

        return new_ally_tiles, new_enemy_tiles, new_human_tiles, conflict_occured
        
    
    def compute_all_possibilities(self, ally_tiles, target_tiles, seperation_per_troop=2):
        if len(ally_tiles) == 1:
            possibilities = []
            orders_for_one_tile = self.compute_orders_for_one_tile(ally_tiles[0], target_tiles, seperation_per_troop)
            for order in orders_for_one_tile:
                possibilities.append([order])
            return possibilities
        else:
            ally = ally_tiles[0]
            sub_possibilities = self.compute_all_possibilities(ally_tiles[1:], target_tiles, seperation_per_troop)
            possibilities = []
            for order in self.compute_orders_for_one_tile(ally, target_tiles, seperation_per_troop):
                for poss in sub_possibilities:
                    possibilities.append([order] + poss)
            return possibilities


    def compute_orders_for_one_tile(self, ally, targets, seperation_per_troop=2):
        enumeration = []
        if seperation_per_troop == 2:
            if ally.nb % 2 == 1:
                for i in range(len(targets)):
                    vector = [0]*len(targets)
                    vector[i] = ally.nb
                    enumeration.append(vector)
                    for j in range(len(targets)):
                        vector = [0]*len(targets)
                        if i!=j:
                            vector[i] = ally.nb // 2
                            vector[j] = ally.nb - ally.nb // 2
                            enumeration.append(vector)
            else:
                for i in range(len(targets)):
                    for j in range(len(targets)):
                        if j >= i:
                            vector = [0]*len(targets)
                            vector[i] = ally.nb // 2
                            vector[j] = ally.nb // 2
                            enumeration.append(vector)
        elif seperation_per_troop == 1:
            for i in range(len(targets)):
                vector = [0]*len(targets)
                vector[i] = ally.nb
                enumeration.append(vector)
        return enumeration

    def check_interesting_possibility(self, poss, ally_tiles, enemy_tiles, human_tiles):
        ''' Return True if the given possibility is an interesting one
        '''
        # Check that the targets are indeed outnumbered
        for (i,ally) in enumerate(ally_tiles):
            for (j,target) in enumerate(ally_tiles + enemy_tiles + human_tiles):
                if poss[i][j] != 0:
                    if j >= len(ally_tiles) and poss[i][j] <= target.nb:
                        return False
        # Check that not all the allies target each other
        poss_matrix = np.array(poss)
        enemy_and_human_targeting_matrix = poss_matrix[0:len(poss_matrix),len(poss_matrix):len(poss_matrix[0])].copy()
        a,b = enemy_and_human_targeting_matrix.shape
        at_least_one_non_ally_target =  not((enemy_and_human_targeting_matrix == np.zeros((a,b))).all())
        return at_least_one_non_ally_target

    def compute_distance(self, tile1, tile2):
        return max(abs(tile1.x-tile2.x), abs(tile1.y-tile2.y))


    def compute_steps(self, x, y, x_target, y_target):
        dir_x = 1 if x_target > x else -1 if x_target < x else 0
        dir_y = 1 if y_target > y else -1 if y_target < y else 0
        return dir_x, dir_y

    def heuristic4(self, ally_tiles, enemy_tiles, human_tiles, faction, previous_ally_tiles, previous_enemy_tiles):
        eating_humans_coef = self.coefs[0] 
        faction_diff_coef = self.coefs[1]
        turn_differential_coef = self.coefs[2]
        split_coef = self.coefs[3]
        # Case where the enemy has been slain
        if faction == BoardTile.ally_faction and len(enemy_tiles) == 0:
            return inf
        elif faction != BoardTile.ally_faction and len(ally_tiles) == 0:
            return inf
        humans_next_to_allies = []
        humans_next_to_enemies = []
        score = 0
        for human in human_tiles:
            try:
                closest_ally = min([self.compute_distance(human,ally) for ally in ally_tiles if ally.nb > human.nb])
            except:
                closest_ally = inf
            try:
                closest_enemy = min([self.compute_distance(human,enemy) for enemy in enemy_tiles if enemy.nb > human.nb])
            except:
                closest_enemy = inf
            if closest_ally == closest_enemy :
                if faction == BoardTile.ally_faction:
                    humans_next_to_allies.append(human.nb)
                else:
                    humans_next_to_enemies.append(human.nb)
            elif closest_ally < closest_enemy:
                humans_next_to_allies.append(human.nb)
            else:
                humans_next_to_enemies.append(human.nb)
        try:
            score += eating_humans_coef*max([s for s in self.enumerate_sub_sums(humans_next_to_allies) if s < sum([a.nb for a in ally_tiles])])
        except :
            pass
        try:
            score -= eating_humans_coef*max([s for s in self.enumerate_sub_sums(humans_next_to_enemies) if s < sum([e.nb for e in enemy_tiles])])
        except:
            pass
        if faction == BoardTile.ally_faction:
            score += faction_diff_coef*(sum([a.nb for a in ally_tiles]) - sum([e.nb for e in enemy_tiles]))
            # score is better if the number of allies (respec. enemies) is higher (respec. lower) than the previous turn 
            score += turn_differential_coef*(sum([a.nb for a in ally_tiles]) - sum([a.nb for a in previous_ally_tiles]))
            score -= turn_differential_coef*(sum([e.nb for e in enemy_tiles]) - sum([e.nb for e in previous_enemy_tiles]))
            # taking into account the number of splits
            score -= split_coef*(len(ally_tiles))
            score += split_coef*(len(enemy_tiles))
        else:
            #symetrical case
            score -= faction_diff_coef*(sum(([a.nb for a in ally_tiles])) - sum(([e.nb for e in enemy_tiles])))
            score -= turn_differential_coef*(sum([a.nb for a in ally_tiles]) - sum([a.nb for a in previous_ally_tiles]))
            score += turn_differential_coef*(sum([e.nb for e in enemy_tiles]) - sum([e.nb for e in previous_enemy_tiles]))
            score += split_coef*(len(ally_tiles))
            score -= split_coef*(len(enemy_tiles))
        return score


    def enumerate_sub_sums(self, liste):
        n = len(liste)
        n_sub_sums = 2**n
        for i in range(n_sub_sums):
            combinaison = [(i // 2**k) % 2 for k in range(n)]
        return combinaison
