from copy import deepcopy
import numpy as np

class order_node():
    id_node=0
    def __init__(self, assigned_paths, assigned_nb, required, potential_paths, depth=0, id_parent=0):
        self.assigned_paths = assigned_paths  # all the paths that have troops assigned so far
        self.assigned_nb = assigned_nb  # list of assigned_nb[i]=nb meaning assigned_paths[i] has been assigned nb troops from tile source_tile
        self.required = required  # dict {tile.id:nb} meaning already nb troops have been required for currently assigned paths from tile 
        self.gain = sum([p.ending_score-p.starting_score for p in self.assigned_paths])
        self.new_potential_paths=[p for p in potential_paths if p.starting_score <= p.source.nb - required[p.source.id]]
        self.depth=depth
        self.id_node=order_node.id_node    
        order_node.id_node+=1    
        
        
        print("node : {} assigned paths, {} potential paths, {} after filtering".format( 
                                        len(assigned_paths),
                                        len(potential_paths), 
                                        len(self.new_potential_paths)))
        print("Node {} at depth {}, son of {}:".format(self.id_node, self.depth, id_parent))
        print("{} assigned paths : ".format(len(assigned_paths)))
        for p in assigned_paths:
            print(p)
        print()
        print("{} potential paths : ".format(len(potential_paths)))
        if(len(potential_paths)>0):
            for p in potential_paths:
                print(p)
            print("{} after filtering".format(len(self.new_potential_paths)))
        print()
        
    def create_sons(self):
        self.sons=[]
        for pot_path in self.new_potential_paths:
            new_required_dic = deepcopy(self.required)
            new_required_dic[pot_path.source.id]+=pot_path.starting_score

            potential_paths_shortened=[]
            for p in self.new_potential_paths:
                path_shortened = p.clone()
                path_shortened.remove_dests(pot_path.dests)

                if len(path_shortened.dests) != 0:
                    redundant=False
                    for dest in path_shortened.dests:
                        for prev_short_path in potential_paths_shortened:
                            if dest in prev_short_path.dests:
                                redundant=True
                                break
                        if redundant:
                            break
                    if not redundant:
                        potential_paths_shortened += [path_shortened]
                
            son = order_node(self.assigned_paths+[pot_path],  # shouldn't need a deep copy since we don't modify the values already in place
                             self.assigned_nb+[pot_path.starting_score],  # idem
                             new_required_dic,
                             potential_paths_shortened,
                             self.depth+1,
                             self.id_node
                             )
            self.sons += [son]
        for s in self.sons:
            s.create_sons()
        
            
    def get_best_gain(self):
        """
        return the gain once each assigned path has been completed
        """
        best_son=self
        best_gain= self.gain
        for s in self.sons:
            son_gain, best_grandson = s.get_best_gain()
            if son_gain > best_gain:
                best_son = best_grandson
                best_gain = son_gain
        # print("Node {} : {}\t-\tBest son {} : {}".format(self.id_node, self.gain, best_son.id_node, best_gain))
                
        return best_gain, best_son
            
            
            
    def __repr__(self):
        s=""
        L = len(self.assigned_paths)
        for i in range(L):
            s += "{} units from ({},{}) for path : {}\n".format(self.assigned_nb[i],
                                                            self.assigned_paths[i].source.x,
                                                            self.assigned_paths[i].source.y,
                                                            self.assigned_paths[i])
        if s == "":
            s="nothing assigned"
        return s    
        
            