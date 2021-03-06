from enum import Enum

class Faction(Enum):
    EMPT = 0
    WERE = 1
    VAMP = 2
    HUM = 3

class Relation(Enum):
    EMPT = 0
    ALLY = 1
    ENEMY = 2
    HUM = 3


class BoardTile():
    ally_faction = Faction.EMPT
    """ Represents a single tile from the board """
    def __init__(self, x, y, nb=0, faction=Faction.EMPT):
        self.__x = x
        self.__y = y
        self.nb = nb
        self.faction=faction
        self.id = (x,y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def relation(self):
        assert self.ally_faction in [Faction.WERE, Faction.VAMP]
        if self.faction == Faction.HUM:
            return Relation.HUM
        if self.faction == Faction.WERE:
            return Relation.ALLY if self.ally_faction == Faction.WERE else Relation.ENEMY
        if self.faction == Faction.VAMP:
            return Relation.ALLY if self.ally_faction == Faction.VAMP else Relation.ENEMY
        return Relation.EMPT

    def __copy__(self):
        return BoardTile(self.__x, self.__y, self.nb, self.faction)

    def copy(self):
        return BoardTile(self.__x, self.__y, self.nb, self.faction)

    def __str__(self):
        if self.faction == Faction.EMPT:
            return "__"
        faction_str = "W" if self.faction == Faction.WERE else "V" if self.faction == Faction.VAMP else "H"
        return str(self.nb)+faction_str

    def __repr__(self):
        return self.__str__()

    def string_all(self):
        return "BoardTile : ({}-{}), nb = {}, faction = {}".format(self.__x, self.__y, self.nb, self.faction)

    def distance(tile1, tile2):
        return max(abs(tile1.x-tile2.x), abs(tile1.y-tile2.y))
