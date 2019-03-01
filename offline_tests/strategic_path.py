
class strategic_path():
    
    def __init__(self, source_tile=None):
        self.source = source_tile
        self.reset()
              
    def reset(self):
        self.dests=[]
        self.total_time=0
        self.times=[]
        self.starting_score=0  # the nb of units you have to send in order to complete this path
        self.ending_score=0
        
    def add_dest(self, target):
        last_dest = self.dests[-1] if len(self.dests)>=1 else self.source
        delta_t = dist(last_dest, target)
        self.dests += [target]
        
        self.total_time += delta_t
        self.times += [delta_t]
        if self.ending_score < target.nb+1: 
            self.starting_score += target.nb+1 - self.ending_score  # we have to send more troops to fulfill this path
            self.ending_score = 2*target.nb+1  # we started with the minimum to take the last humans on the list so we end with the minimum
        else:
            self.ending_score += target.nb
        
    
    def remove_dests(self, targets):
        new_dests = []
        change = False
        for d in self.dests:
            if d in targets:
                change=True
            else:
                new_dests+=[d]
        if change:
            self.reset()
            for d in new_dests:
                self.add_dest(d)
        
    def __str__(self):
        s = "[{}] ".format(self.starting_score)
        time_spent = 0
        s += "({},{} - {})".format(self.source.x, self.source.y, self.source)
        for i, tile in enumerate(self.dests):
            time_spent += self.times[i]
            s += " -> ({},{} - {} - {}t)".format(tile.x, tile.y, tile, time_spent)
        s += " [{}]".format(self.ending_score)
        return s
    
    def __repr__(self):
        return self.__str__()
    
    def clone(self):
        r = strategic_path(source_tile=self.source)
        r.dests = [d for d in self.dests]
        r.total_time = self.total_time
        r.times = [t for t in self.times]
        r.starting_score = self.starting_score
        r.ending_score = self.ending_score
        return r
    
    
    
    
    
def dist(tile1, tile2):  # returns the distance between two tiles
    return max(abs(tile1.x - tile2.x), abs(tile1.y-tile2.y))
    