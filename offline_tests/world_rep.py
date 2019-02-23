from time import time
import numpy as np
import sys
import os 

sys.path.append(os.path.dirname(os.path.join(os.path.realpath(__file__),"../")))  
from board_tile import board_tile



def get_tiles_of_interest(board):
    tiles_of_interest = {"VAMP":[], "WERE":[], "HUM":[]}
    for row in board:
        for tile in row:
            if tile.faction != "EMPT":
                tiles_of_interest[tile.faction] += [tile]
    return tiles_of_interest
    
    
def dist(tile1, tile2):  # returns the distance between two tiles
    return max(abs(tile1.x - tile2.x), abs(tile1.y-tile2.y))
    

def get_crit_time(target, enemy_tiles): 
    """
    returns the time we have before the given target tile gets potentially compromised by an enemy batalion
    """
    try :
        return min([dist(tile, target) for tile in enemy_tiles if tile.nb>target.nb])
    except:
        return np.inf
        
def get_potential_targets(source_tile, enemy_tiles, human_tiles, delay=0):
    """
    For a given source tile belonging to us,
    returns the humans tiles it can get to before they get compromised by enemies
    optionnal delay to get the same result considering we need some time before leaving from source_tile
    """
    return [target for target in human_tiles if get_crit_time(target, enemy_tiles)>dist(source_tile, target)+delay]
    

    
def get_all_paths(source_tile, enemy_tiles, target_tiles, current_path=[], time_spent=0):
    """
    returns all possible paths from a source tile sending one bataillon 
    to get any number of targets amongst the potential target
    the paths must never go through a compromised tile
    """
    
    if target_tiles == []:
        return [current_path]

    all_paths = []
    for i, target in enumerate(target_tiles):
        potential_path = current_path+[target]
        time_spent += dist(source_tile,target)
        new_target_tiles = get_potential_targets(target, enemy_tiles, target_tiles[:i]+target_tiles[i+1:], delay=time_spent)
        
        all_paths += get_all_paths(target, enemy_tiles, new_target_tiles, potential_path, time_spent)
    return all_paths
    
    

        
        
    