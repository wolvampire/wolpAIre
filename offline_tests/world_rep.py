from time import time
import numpy as np
import sys
import os 

from board_tile import board_tile
from strategic_path import strategic_path



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
        return min([dist(tile, target) for tile in enemy_tiles])
    except:
        return np.inf
        
def get_potential_targets(source_tile, enemy_tiles, human_tiles, delay=0):
    """
    For a given source tile belonging to us,
    returns the humans tiles it can get to before they get compromised by enemies
    optionnal delay to get the same result considering we need some time before leaving from source_tile
    """
    return [target for target in human_tiles if get_crit_time(target, enemy_tiles)>=dist(source_tile, target)+delay]
    

    
def get_all_paths(source_tile, enemy_tiles, target_tiles, current_path=None, time_spent=0):
    """
    returns all possible paths from a source tile sending one bataillon 
    to get any number of targets amongst the potential target
    the paths must never go to a compromised tile
    """
    if current_path is None:
        current_path = strategic_path(source_tile=source_tile)
        
    if target_tiles == []:
        if len(current_path.dests)==0:
            return []
        return [current_path]
        
    if len(current_path.dests)>3:
        return [current_path]

    all_paths = []
    for i, target in enumerate(target_tiles):
        potential_path = current_path.clone()
        potential_path.add_dest(target)
        new_time_spent = time_spent + dist(source_tile,target)
        new_target_tiles = get_potential_targets(target, enemy_tiles, target_tiles[:i]+target_tiles[i+1:], delay=new_time_spent)
        all_paths += get_all_paths(target, enemy_tiles, new_target_tiles, potential_path, new_time_spent)
        
    return all_paths
    
    

        
        
    