#!/usr/bin/python

# a male individual
class Male(object):
    #TODO
    """
        qualities:
            maturation time:
            energy at maturation
            mass at maturation
        
        heriditable traits:
            lambda 
            psi
            aggression

        costs:
            metabolic
            predation

        events:
            contests
            searching
            abandoning
    """
    # constructor
    def __init__(self, params, mom = None, dad = None):
        if not mom and not dad: # first gen no breeding
            self.lambda_ = 0
        else:
            # gentetic breeding 

    # the outcome of a contest is created here
    def contest(self, opponent):
        
