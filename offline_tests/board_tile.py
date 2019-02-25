


class board_tile():
    """ Represents a single tile from the board """
    def __init__(self, x, y, nb=0, faction="EMPT"):
        self.x = x
        self.y = y
        self.nb=nb
        self.faction=faction  # among "WERE", "VAMP", "HUM" (for humans), "EMPT"
        self.id = int(str(x)+str(y))
        
    def __str__(self):
        if self.faction == "EMPT":
            return "__"
        faction_str = "L" if self.faction == "WERE" else "V" if self.faction == "VAMP" else "H"
        return str(self.nb)+faction_str
        
    def __repr__(self):
        return self.__str__()