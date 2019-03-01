from enum import Enum

class Faction(Enum):
    EMPT = 0
    WERE = 1
    VAMP = 2
    HUM = 3

class board_tile():
    """ Represents a single tile from the board """
    def __init__(self, x, y, nb=0, faction=Faction.EMPT):
        self.x = x
        self.y = y
        self.nb=0
        self.faction=faction
        
        
