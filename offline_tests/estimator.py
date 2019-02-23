def get_attack_result(nb_att, nb_def):
    """
    returns the probability P of victory if we attack the other player, 
    and the expecting surviving troops for us and for them
    """
    p = min(1,max(nb_att/(2*nb_def), nb_att/nb_def-0.5))  # rules in the pdf
    exp_us = p*p*nb_att  # probability p of winning and then each unit has p of surviving
    exp_them = (1-p)*(1-p)*nb_def
    return p, exp_us, exp_them
    
    
def get_human_result(nb_att, nb_def):
    """
    returns the probability P of victory if we attack humans,
    and the expecting surviving troops for us and for them
    """
    
    p = 1 if nb_att>nb_def else nb_att/(2*nb_def)
    exp_us = p*p*nb_att + p*nb_def  # probability p of winning and then each unit has p of surviving and each human has p of turning into us
    exp_them = (1-p)*(1-p)*nb_def
    return p, exp_us, exp_them