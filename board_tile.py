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
        
        
    def __str__(self):
        if self.faction == Faction.EMPT:
            return "__"
        faction_str = "L" if self.faction == Faction.WERE else "V" if self.faction == Faction.VAMP else "H"
        return str(self.nb)+faction_str
        
    def __repr__(self):
        return self.__str__()